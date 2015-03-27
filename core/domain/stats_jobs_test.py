# coding: utf-8
#
# Copyright 2014 The Oppia Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__author__ = 'Stephanie Federwisch'

"""Tests for statistics continuous computations."""

from core import jobs_registry
from core.domain import event_services
from core.domain import exp_services
from core.domain import stats_jobs
from core.platform import models
(stats_models, exp_models) = models.Registry.import_models([models.NAMES.statistics, models.NAMES.exploration])
from core.tests import test_utils
import feconf
from datetime import datetime


class ModifiedStatisticsAggregator(stats_jobs.StatisticsAggregator):
    """A modified StatisticsAggregator that does not start a new batch
    job when the previous one has finished.
    """
    @classmethod
    def _get_batch_job_manager_class(cls):
        return ModifiedStatisticsMRJobManager

    @classmethod
    def _kickoff_batch_job_after_previous_one_ends(cls):
        pass


class ModifiedStatisticsMRJobManager(stats_jobs.StatisticsMRJobManager):

    @classmethod
    def _get_continuous_computation_class(cls):
        return ModifiedStatisticsAggregator


class OneOffFixStartCounts(test_utils.GenericTestBase):
    def test_job(self):
        exp_id = 'eid'
        exploration = self.save_new_valid_exploration(exp_id, 'owner')
        first_init_state = exploration.init_state_name

        first_state_counter = (
            stats_models.StateCounterModel.get_or_create(exp_id, first_init_state))
        first_state_counter.first_entry_count = 17
        first_state_counter.put()

        for _ in range(17):
            entity_id = stats_models.StartExplorationEventLogEntryModel.create(
                exp_id, 1, first_init_state, 'session_id', {}, feconf.PLAY_TYPE_NORMAL)
            entity = stats_models.StartExplorationEventLogEntryModel.get(entity_id)
            entity.created_on = datetime(2014, 10, 5)
            entity.put()

        second_init_state = 'second init state'
        exploration.rename_state(first_init_state, second_init_state)
        exp_services._save_exploration('person', exploration, 'message', None)
        metadata = exp_models.ExplorationSnapshotMetadataModel.get('%s-%s' % (
            exp_id, 2))
        metadata.created_on = datetime(2014, 10, 6)
        metadata.put()

        for _ in range(13):
            entity_id = stats_models.StartExplorationEventLogEntryModel.create(
                exp_id, 2, second_init_state, 'session_id', {}, feconf.PLAY_TYPE_NORMAL)
            entity = stats_models.StartExplorationEventLogEntryModel.get(entity_id)
            entity.created_on = datetime(2014, 10, 7)
            entity.put()
        
        second_state_counter = (
            stats_models.StateCounterModel.get_or_create(exp_id, second_init_state))
        second_state_counter.first_entry_count = -17
        second_state_counter.put()

        for _ in range(19):
            entity_id = stats_models.StartExplorationEventLogEntryModel.create(
                exp_id, 1, second_init_state, 'session_id', {}, feconf.PLAY_TYPE_NORMAL)
            entity = stats_models.StartExplorationEventLogEntryModel.get(entity_id)
            entity.created_on = datetime(2014, 10, 19)
            entity.put()

        job_id = stats_jobs.OneOffFixStartCounts.create_new()
        stats_jobs.OneOffFixStartCounts.enqueue(job_id)
        self.process_and_flush_pending_tasks()

        first_state_counter = (
            stats_models.StateCounterModel.get_or_create(exp_id, first_init_state))
        self.assertEqual(first_state_counter.first_entry_count, 0)
        second_state_counter = (
            stats_models.StateCounterModel.get_or_create(exp_id, second_init_state))
        self.assertEqual(second_state_counter.first_entry_count, 0)

        job_id = stats_jobs.OneOffFixStartCounts.create_new()
        stats_jobs.OneOffFixStartCounts.enqueue(job_id)
        self.process_and_flush_pending_tasks()

        first_state_counter = (
            stats_models.StateCounterModel.get_or_create(exp_id, first_init_state))
        self.assertEqual(first_state_counter.first_entry_count, 0)
        second_state_counter = (
            stats_models.StateCounterModel.get_or_create(exp_id, second_init_state))
        self.assertEqual(second_state_counter.first_entry_count, 0)



class StatsAggregatorUnitTests(test_utils.GenericTestBase):
    """Tests for statistics aggregations."""

    ALL_CONTINUOUS_COMPUTATION_MANAGERS_FOR_TESTS = [
        ModifiedStatisticsAggregator]

    def _record_start(self, exp_id, exp_version, state, session_id):
        event_services.StartExplorationEventHandler.record(
            exp_id, exp_version, state, session_id, {},
            feconf.PLAY_TYPE_NORMAL)

    def _record_leave(self, exp_id, exp_version, state, session_id):
        event_services.MaybeLeaveExplorationEventHandler.record(
            exp_id, exp_version, state, session_id, 27, {},
            feconf.PLAY_TYPE_NORMAL)

    def test_no_completion(self):
        with self.swap(
                jobs_registry, 'ALL_CONTINUOUS_COMPUTATION_MANAGERS',
                self.ALL_CONTINUOUS_COMPUTATION_MANAGERS_FOR_TESTS):
            exp_id = 'eid'
            exp_version = 1
            exploration = self.save_new_valid_exploration(exp_id, 'owner')
            state = exploration.init_state_name

            self._record_start(exp_id, exp_version, state, 'session1')
            self._record_start(exp_id, exp_version, state, 'session2')
            self.process_and_flush_pending_tasks()

            ModifiedStatisticsAggregator.start_computation()
            self.assertEqual(self.count_jobs_in_taskqueue(), 1)
            self.process_and_flush_pending_tasks()

            model_id = '%s:%s' % (exp_id, exp_version)
            output_model = stats_models.ExplorationAnnotationsModel.get(
                model_id)
            self.assertEqual(output_model.num_starts, 2)
            self.assertEqual(output_model.num_completions, 0)

    def test_all_complete(self):
        with self.swap(
                jobs_registry, 'ALL_CONTINUOUS_COMPUTATION_MANAGERS',
                self.ALL_CONTINUOUS_COMPUTATION_MANAGERS_FOR_TESTS):
            exp_id = 'eid'
            exp_version = 1
            exploration = self.save_new_valid_exploration(exp_id, 'owner')
            state = exploration.init_state_name

            self._record_start(exp_id, exp_version, state, 'session1')
            self._record_leave(
                exp_id, exp_version, feconf.END_DEST, 'session1')
            self._record_start(exp_id, exp_version, state, 'session2')
            self._record_leave(
                exp_id, exp_version, feconf.END_DEST, 'session2')
            self.process_and_flush_pending_tasks()

            ModifiedStatisticsAggregator.start_computation()
            self.assertEqual(self.count_jobs_in_taskqueue(), 1)
            self.process_and_flush_pending_tasks()

            model_id = '%s:%s' % (exp_id, exp_version)
            output_model = stats_models.ExplorationAnnotationsModel.get(
                model_id)
            self.assertEqual(output_model.num_starts, 2)
            self.assertEqual(output_model.num_completions, 2)

    def test_multiple_maybe_leaves_same_session(self):
        with self.swap(
                jobs_registry, 'ALL_CONTINUOUS_COMPUTATION_MANAGERS',
                self.ALL_CONTINUOUS_COMPUTATION_MANAGERS_FOR_TESTS):
            exp_id = 'eid'
            exp_version = 1
            exploration = self.save_new_valid_exploration(exp_id, 'owner')
            state = exploration.init_state_name

            self._record_start(exp_id, exp_version, state, 'session1')
            self._record_leave(exp_id, exp_version, state, 'session1')
            self._record_leave(exp_id, exp_version, state, 'session1')
            self._record_leave(
                exp_id, exp_version, feconf.END_DEST, 'session1')

            self._record_start(exp_id, exp_version, state, 'session2')
            self._record_leave(exp_id, exp_version, state, 'session2')
            self._record_leave(exp_id, exp_version, state, 'session2')
            self.process_and_flush_pending_tasks()

            ModifiedStatisticsAggregator.start_computation()
            self.assertEqual(self.count_jobs_in_taskqueue(), 1)
            self.process_and_flush_pending_tasks()

            model_id = '%s:%s' % (exp_id, exp_version)
            output_model = stats_models.ExplorationAnnotationsModel.get(
                model_id)
            self.assertEqual(output_model.num_starts, 2)
            self.assertEqual(output_model.num_completions, 1)

    def test_multiple_explorations(self):
        with self.swap(
                jobs_registry, 'ALL_CONTINUOUS_COMPUTATION_MANAGERS',
                self.ALL_CONTINUOUS_COMPUTATION_MANAGERS_FOR_TESTS):

            exp_version = 1
            exp_id_1 = 'eid1'
            exploration = self.save_new_valid_exploration(exp_id_1, 'owner')
            state_1_1 = exploration.init_state_name
            exp_id_2 = 'eid2'
            exploration = self.save_new_valid_exploration(exp_id_2, 'owner')
            state_2_1 = exploration.init_state_name

            EMPTY_STATE_HIT_COUNTS_DICT = {
                'First State': {
                    'total_entry_count': 0,
                    'no_answer_count': 0,
                    'first_entry_count': 0,
                },
            }

            # Record 2 start events for exp_id_1 and 1 start event for
            # exp_id_2.
            self._record_start(exp_id_1, exp_version, state_1_1, 'session1')
            self._record_start(exp_id_1, exp_version, state_1_1, 'session2')
            self._record_start(exp_id_2, exp_version, state_2_1, 'session3')
            self.process_and_flush_pending_tasks()
            ModifiedStatisticsAggregator.start_computation()
            self.assertEqual(self.count_jobs_in_taskqueue(), 1)
            self.process_and_flush_pending_tasks()
            results = ModifiedStatisticsAggregator.get_statistics(
                exp_id_1, 'all')
            self.assertDictContainsSubset({
                'start_exploration_count': 2,
                'complete_exploration_count': 0,
                'state_hit_counts': EMPTY_STATE_HIT_COUNTS_DICT,
            }, results)
            results = ModifiedStatisticsAggregator.get_statistics(
                exp_id_2, 'all')
            self.assertDictContainsSubset({
                'start_exploration_count': 1,
                'complete_exploration_count': 0,
                'state_hit_counts': EMPTY_STATE_HIT_COUNTS_DICT,
            }, results)

            # Record 1 more start event for exp_id_1 and 1 more start event
            # for exp_id_2.
            self._record_start(exp_id_1, exp_version, state_1_1, 'session2')
            self._record_start(exp_id_2, exp_version, state_2_1, 'session3')
            self.process_and_flush_pending_tasks()
            results = ModifiedStatisticsAggregator.get_statistics(
                exp_id_1, 'all')
            self.assertDictContainsSubset({
                'start_exploration_count': 3,
                'complete_exploration_count': 0,
                'state_hit_counts': EMPTY_STATE_HIT_COUNTS_DICT,
            }, results)
            results = ModifiedStatisticsAggregator.get_statistics(
                exp_id_2, 'all')
            self.assertDictContainsSubset({
                'start_exploration_count': 2,
                'complete_exploration_count': 0,
                'state_hit_counts': EMPTY_STATE_HIT_COUNTS_DICT,
            }, results)
