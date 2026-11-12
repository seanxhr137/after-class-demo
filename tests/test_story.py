import copy
import json
import unittest
from pathlib import Path
from tools.check_story import validate_story

ROOT = Path(__file__).resolve().parents[1]

class StoryTests(unittest.TestCase):
    def setUp(self):
        self.story = json.loads((ROOT / 'story.json').read_text())

    def test_current_story_reaches_endings(self):
        result = validate_story(self.story)
        self.assertGreaterEqual(result['endings'], 1)

    def test_changed_text_and_new_route_are_valid(self):
        self.story['nodes'][0]['text'] = '这是协作者通过网页修改的一句台词。'
        node = next(n for n in self.story['nodes'] if 'choices' in n)
        node['choices'][0]['route'] = 'new_route'
        validate_story(self.story)

    def test_missing_target_is_blocked(self):
        self.story['nodes'][0]['next'] = 'not-present'
        with self.assertRaisesRegex(ValueError, '跳转'):
            validate_story(self.story)

    def test_duplicate_id_is_blocked(self):
        self.story['nodes'][1]['id'] = self.story['nodes'][0]['id']
        with self.assertRaisesRegex(ValueError, '重复'):
            validate_story(self.story)

    def test_missing_image_is_blocked(self):
        self.story['actors']['me']['image'] = 'assets/does-not-exist.png'
        with self.assertRaisesRegex(ValueError, '找不到文件'):
            validate_story(self.story)

    def test_dead_end_is_blocked(self):
        self.story['nodes'][0].pop('next')
        with self.assertRaisesRegex(ValueError, '必须且只能'):
            validate_story(self.story)

if __name__ == '__main__':
    unittest.main()
