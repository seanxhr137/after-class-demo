"""Validate the actual editable story and its resource references before deployment."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def validate_story(data, root=ROOT):
    def require(condition, message):
        if not condition:
            raise ValueError(message)

    def resource(value, where):
        if value is None:
            return
        require(isinstance(value, str) and value.startswith('assets/'), f'{where}: 路径必须从 assets/ 开始')
        target = (root / value).resolve()
        require(target.is_relative_to((root / 'assets').resolve()), f'{where}: 路径超出 assets')
        require(target.is_file(), f'{where}: 找不到文件 {value}')

    require(isinstance(data, dict), '剧情顶层必须是对象')
    require(isinstance(data.get('id'), str) and data['id'], '缺少故事 id')
    require(data.get('version') == 4, 'version 必须保留为 4')
    actors, lines = data.get('actors'), data.get('nodes')
    require(isinstance(actors, dict) and 'me' in actors, 'actors 必须包含主角 me')
    for key, actor in actors.items():
        require(isinstance(actor, dict) and isinstance(actor.get('name'), str), f'角色 {key}: 缺少 name')
        require(isinstance(actor.get('tag'), str), f'角色 {key}: 缺少 tag')
        require(isinstance(actor.get('color'), str) and len(actor['color']) == 7 and actor['color'].startswith('#') and all(c in '0123456789abcdefABCDEF' for c in actor['color'][1:]), f'角色 {key}: color 应为 #RRGGBB')
        resource(actor.get('image'), f'角色 {key}')
        require(isinstance(actor.get('expressions', {}), dict), f'角色 {key}: expressions 必须是对象')
        for emotion, image in actor.get('expressions', {}).items():
            resource(image, f'角色 {key}/{emotion}')
    require(isinstance(lines, list) and len(lines) > 0, 'nodes 必须是非空数组')
    ids = set()
    for line in lines:
        require(isinstance(line, dict), '每句台词必须是对象')
        key = line.get('id')
        require(isinstance(key, str) and key and key not in ids, f'台词 id 为空或重复: {key}')
        ids.add(key)
    require(data.get('start') in ids, 'start 指向不存在的台词')
    graph, endings = {}, set()
    for line in lines:
        key = line['id']
        require(isinstance(line.get('text'), str) and line['text'].strip(), f'{key}: text 不能为空')
        require(line.get('speaker') in actors or line.get('speaker') in ['thought', 'narration'], f'{key}: speaker 不是已定义角色')
        require(isinstance(line.get('chapter'), str), f'{key}: 缺少 chapter')
        require(isinstance(line.get('bg'), str) and '/' not in line['bg'], f'{key}: bg 应为背景文件名，不带路径与扩展名')
        resource('assets/' + line['bg'] + '.jpg', key)
        cast = line.get('cast')
        require(isinstance(cast, list) and len(cast) <= 2, f'{key}: cast 应为最多两个角色的数组')
        positions = set()
        for member in cast:
            require(isinstance(member, dict) and member.get('actor') in actors, f'{key}: cast 中角色不存在')
            position = member.get('position')
            require(position in ['left', 'right'] and position not in positions, f'{key}: 站位无效或重复')
            positions.add(position)
            require(isinstance(member.get('expression'), str), f'{key}: 缺少 expression')
        for media in ['voice', 'bgm']:
            if media in line:
                resource(line[media], f'{key}/{media}')
        exits = sum(k in line for k in ['next', 'choices', 'ending'])
        require(exits == 1, f'{key}: next、choices、ending 必须且只能出现一种')
        targets = []
        if 'next' in line:
            targets.append(line['next'])
        if 'choices' in line:
            choices = line['choices']
            require(isinstance(choices, list) and 2 <= len(choices) <= 4, f'{key}: 选项数量需为 2-4')
            for choice in choices:
                require(isinstance(choice, dict) and isinstance(choice.get('text'), str) and choice['text'], f'{key}: 选项缺少 text')
                require(isinstance(choice.get('route'), str) and choice['route'], f'{key}: 选项缺少 route')
                targets.append(choice.get('next'))
        if 'ending' in line:
            end = line['ending']
            require(isinstance(end, dict) and all(isinstance(end.get(k), str) and end[k] for k in ['id', 'title', 'text']), f'{key}: 结尾缺少 id、title 或 text')
            endings.add(key)
        require(all(isinstance(t, str) and t in ids for t in targets), f'{key}: 跳转到不存在的台词')
        graph[key] = targets
    reached, queue = set(), [data['start']]
    while queue:
        key = queue.pop()
        if key in reached:
            continue
        reached.add(key)
        queue.extend(graph[key])
    require(reached == ids, '有无法从开始到达的台词: ' + ', '.join(sorted(ids - reached)))
    can_end = set(endings)
    while True:
        previous = len(can_end)
        can_end.update(k for k, targets in graph.items() if any(t in can_end for t in targets))
        if previous == len(can_end):
            break
    require(can_end == ids, '存在无法到达任何结局的剧情路径')
    return {'lines': len(lines), 'choice_points': sum('choices' in n for n in lines), 'endings': len(endings)}


if __name__ == '__main__':
    try:
        data = json.loads((ROOT / 'story.json').read_text(encoding='utf-8'))
        print('剧情检查通过:', json.dumps(validate_story(data), ensure_ascii=False))
    except (ValueError, KeyError, TypeError) as error:
        raise SystemExit('剧情检查失败: ' + str(error))
