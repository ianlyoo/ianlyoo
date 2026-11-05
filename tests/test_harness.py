import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('harness',ROOT/'tools'/'harness.py')
harness=importlib.util.module_from_spec(spec)
spec.loader.exec_module(harness)

class HarnessTests(unittest.TestCase):
    def test_profiles_have_exactly_three_workers(self):
        for slug,conf in harness.CONFIG['profiles'].items():
            with self.subTest(slug=slug):
                self.assertEqual(len(conf['agents']),3)
                self.assertEqual(len(set(conf['agents'])),3)
                self.assertTrue(set(conf['agents']).issubset(harness.AGENT_ROLES))
                for skill in conf['built_in_skills']:
                    self.assertTrue((ROOT/'skills'/skill/'SKILL.md').is_file(),skill)
                for skill in conf['external_skills']+conf.get('optional_skills',[]):
                    self.assertIn(skill,harness.CONFIG['external_catalog'])

    def test_hybrid_dashboard_routing(self):
        task='''데이터 분석 dashboard를 만들고 dataset CSV 데이터를 검증합니다. 정류장 routing 노선, 최적화 배정, schedule이 필수입니다. 웹 서비스 화면도 필요합니다.'''
        got=harness.route(task)
        self.assertEqual(got['profile'],'fullstack-analytics')
        self.assertEqual(got['agents'],['data-engineer','optimization-engineer','frontend-engineer'])

    def test_predictive_profile(self):
        task='''Forecast forecasting regression classification machine learning time series 시계열 예측 데이터 split 훈련 평가.'''
        got=harness.route(task)
        self.assertEqual(got['profile'],'prediction-ml')
        self.assertEqual(got['agents'][1],'ml-engineer')

    def test_document_intelligence(self):
        task='''PDF documents, XLSX excel sheets, DOCX reports, document extraction 문서 보고서 검증.'''
        got=harness.route(task)
        self.assertEqual(got['profile'],'document-intelligence')

    def test_setup_non_destructive(self):
        with tempfile.TemporaryDirectory() as work:
            w=Path(work)
            (w/'README.md').write_text('Official task: algorithm graph 최적화, routing, constraint.',encoding='utf-8')
            (w/'AGENTS.md').write_text('Official protected context\n',encoding='utf-8')
            (w/'.codex').mkdir()
            (w/'.codex'/'config.toml').write_text('[agents]\nmax_concurrent_threads_per_session = 2\n',encoding='utf-8')
            args=type('Args',(),{'workspace':str(w),'task':'README.md','profile':'auto','agents':'','add_external':'','superpowers':False,'external':False,'dry_run':False})()
            harness.setup(args)
            self.assertEqual((w/'README.md').read_text(encoding='utf-8'),'Official task: algorithm graph 최적화, routing, constraint.')
            self.assertEqual((w/'AGENTS.md').read_text(encoding='utf-8'),'Official protected context\n')
            self.assertEqual((w/'.codex'/'config.toml').read_text(encoding='utf-8'),'[agents]\nmax_concurrent_threads_per_session = 2\n')
            self.assertTrue((w/'.hackathon'/'PROJECT_AGENT_RULES.md').exists())
            self.assertTrue((w/'DECISION_LOG.md').exists())
            self.assertTrue((w/'EXPLAINABILITY_NOTES.md').exists())
            self.assertTrue((w/'VERIFICATION_MATRIX.md').exists())
            self.assertTrue((w/'.agents'/'skills'/'decision-journal'/'SKILL.md').exists())
            old=(w/'DECISION_LOG.md').read_text(encoding='utf-8')
            harness.setup(args)
            self.assertEqual(old,(w/'DECISION_LOG.md').read_text(encoding='utf-8'))

    def test_external_skills_conditional(self):
        p=harness.CONFIG['profiles']['web-product']
        caps={'ui':5,'ml':0,'data':0,'optimization':0,'document':0,'agent':0,'security':0,'simulation':0}
        self.assertNotIn('react-best-practices',harness.external_selection(p,caps,'create dashboard ui website'))
        self.assertIn('react-best-practices',harness.external_selection(p,caps,'create React dashboard ui website'))
        self.assertNotIn('impeccable',harness.external_selection(p,{**caps,'ui':0},'backend API only'))

    def test_task_not_sent_to_shell(self):
        task='PRIVATE USER TASK CONTENT that should never leave machine'
        with tempfile.TemporaryDirectory() as work:
            w=Path(work)
            (w/'README.md').write_text(task,encoding='utf-8')
            args=type('Args',(),{'workspace':str(w),'task':'README.md','profile':'web-product','agents':'','add_external':'','superpowers':False,'external':False,'dry_run':False})()
            with patch.object(harness.subprocess,'run') as run:
                harness.setup(args)
                self.assertEqual(run.call_count,0)
                self.assertFalse((w/'.hackathon'/'START.md').read_text(encoding='utf-8').find(task)>=0)

if __name__=='__main__':
    unittest.main()
