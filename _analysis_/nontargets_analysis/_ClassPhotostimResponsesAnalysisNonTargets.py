import sys

from _analysis_.nontargets_analysis._ClassPhotostimResponseQuantificationNonTargets import \
    PhotostimResponsesQuantificationNonTargets, FakeStimsQuantification
from _exp_metainfo_.exp_metainfo import ExpMetainfo

sys.path.extend(['/home/pshah/Documents/code/AllOpticalSeizure', '/home/pshah/Documents/code/AllOpticalSeizure'])

from typing import Union

import numpy as np
import pandas as pd
from scipy import stats

from matplotlib import pyplot as plt

from _utils_ import _alloptical_utils as Utils
from _main_.AllOpticalMain import alloptical
from _main_.Post4apMain import Post4ap
from funcsforprajay import plotting as pplot


# %% ###### NON TARGETS analysis + plottings


# results: PhotostimResponsesNonTargetsResults = PhotostimResponsesNonTargetsResults.load()


######

class PhotostimResponsesAnalysisNonTargets(PhotostimResponsesQuantificationNonTargets):
    """
    continuation from class: photostim responses quantification nontargets


    [ ] quantify the number of responders that are statistically significant across baseline and interictal (and maybe even out of sz) (as oppossed significant responders within each condition)
    [ ] plotting of significant responders (pos and neg) traces across baseline, interictal and ictal (outsz)

    [i] plotting of significant responders (pos and neg) traces from baseline, during baseline, interictal and ictal (outsz) states


    [ ] fake-sham trials in the analysis for total targets activity vs. total network activity:
        - try plotting without z scoring first for one experiment - and send to Adam on slack.
            - this will allow you to put all the photostim and fakestim responses on one plot (as two separate groups)
                    - then for z scoring you should probably consider z scoring to baseline if you really get to this point....
        [x] create fake sham stim frames - halfway in between each stim trial
        [x] collect photostim targets fake sham responses
            [x] plot peri-stim avg
            [x] plot response magnitude


        [x] collect nontargets fake sham responses
            [x] test for significant responders - came out nil as expected for all nontargets
            [x] plug into plot peri-stim avg for photostim_nontargets analysis
                [ipr] make graph of peri-stim avg with pos significant responders, neg significant responders, fakestims, and nonresponders

        [ ] scatter plot of total nontargets activity and total targets activity


    """

    def __init__(self, expobj: Union[alloptical, Post4ap], results):
        from _analysis_.nontargets_analysis._ClassResultsNontargetPhotostim import PhotostimResponsesNonTargetsResults
        results: PhotostimResponsesNonTargetsResults
        super().__init__(expobj=expobj, results=results)

    @staticmethod
    @Utils.run_for_loop_across_exps(run_pre4ap_trials=1, run_post4ap_trials=1,
                                    allow_rerun=0,
                                    skip_trials=PhotostimResponsesQuantificationNonTargets.EXCLUDE_TRIALS, )
    # run_trials=PhotostimResponsesQuantificationNonTargets.TEST_TRIALS)
    def run__initPhotostimResponsesAnalysisNonTargets(**kwargs):
        expobj: Union[alloptical, Post4ap] = kwargs['expobj']
        expobj.PhotostimResponsesNonTargets = PhotostimResponsesAnalysisNonTargets(expobj=expobj)
        expobj.save()

    # 2.1) PLOT - POS AND NEG SIG RESPONDERS TRACES FOR EXPERIMENT
    # def plot__sig_responders_traces(self, expobj: Union[alloptical, Post4ap]):
    #
    #     from _analysis_._ClassPhotostimAnalysisSlmTargets import PhotostimAnalysisSlmTargets
    #     from _utils_.alloptical_plotting import plot_periphotostim_avg2
    #
    #     if 'pre' in self.expobj_exptype:
    #         pos_avg_traces = [self.pre4ap_possig_responders_avgtraces_baseline]
    #         neg_avg_traces = [self.pre4ap_negsig_responders_avgtraces_baseline]
    #     elif 'post' in self.expobj_exptype:
    #         pos_avg_traces = [self.post4ap_possig_responders_avgtraces_interictal]
    #         neg_avg_traces = [self.post4ap_negsig_responders_avgtraces_interictal]
    #     else:
    #         raise Exception()
    #
    #     fig, axs = plt.subplots(figsize=(4, 6), nrows=2, ncols=1)
    #
    #     if len(pos_avg_traces[0]) > 0:
    #         plot_periphotostim_avg2(dataset=pos_avg_traces, fps=expobj.fps,
    #                                 legend_labels=[f"pos. cells: {len(pos_avg_traces[0])}"],
    #                                 colors=['blue'], avg_with_std=True,
    #                                 suptitle=f"{self.expobj_id} - {self.expobj_exptype} - sig. responders",
    #                                 ylim=[-0.3, 0.8], fig=fig, ax=axs[0],
    #                                 pre_stim_sec=PhotostimAnalysisSlmTargets._pre_stim_sec,
    #                                 show=False, fontsize='small', figsize=(4, 4),
    #                                 xlabel='Time (secs)', ylabel='Avg. Stim. Response (dF/stdF)')
    #     else:
    #         print(f"**** {expobj.t_series_name} has no statistically significant positive responders.")
    #     if len(neg_avg_traces[0]) > 0:
    #         plot_periphotostim_avg2(dataset=neg_avg_traces, fps=expobj.fps,
    #                                 legend_labels=[f"neg. cells: {len(neg_avg_traces[0])}"],
    #                                 colors=['blue'], avg_with_std=True,
    #                                 title=f"{self.expobj_id} - {self.expobj_exptype} - -ve sig. responders",
    #                                 ylim=[-0.6, 0.5], fig=fig, ax=axs[1],
    #                                 pre_stim_sec=PhotostimAnalysisSlmTargets._pre_stim_sec,
    #                                 show=False, fontsize='small', figsize=(4, 4),
    #                                 xlabel='Time (secs)', ylabel='Avg. Stim. Response (dF/stdF)')
    #     else:
    #         print(f"**** {expobj.t_series_name} has no statistically significant negative responders.")
    #
    #     fig.show()

    # 2.2) PLOT - POS AND NEG SIG RESPONDERS TRACES FOR EXPERIMENT
    @staticmethod
    def plot__pos_neg_responders_traces(expobj: alloptical, pos_avg_traces: list = None, neg_avg_traces: list = None,
                                        fake_avg_traces: list = None, title: str = ''):
        """
        Plot avg peri-stim traces of input +ve and -ve responders traces.

        :param title:
        :param fake_avg_traces:
        :param expobj:
        :param pos_avg_traces:
        :param neg_avg_traces:
        """
        if pos_avg_traces is None:
            pos_avg_traces = [[]]
        if neg_avg_traces is None:
            neg_avg_traces = [[]]
        from _analysis_._ClassPhotostimAnalysisSlmTargets import PhotostimAnalysisSlmTargets
        from _utils_.alloptical_plotting import plot_periphotostim_avg2

        same_plot = True

        if not same_plot:
            fig, axs = plt.subplots(figsize=(4, 6), nrows=2, ncols=1)
        else:
            fig, axs = plt.subplots(figsize=(5, 5))

        if len(pos_avg_traces[0]) > 0:
            ax = axs if same_plot else axs[0]
            plot_periphotostim_avg2(dataset=pos_avg_traces, fps=expobj.fps,
                                    # legend_labels=[f"pos. cells: {len(pos_avg_traces[0])}"],
                                    colors=['blue'], avg_with_std=True,
                                    suptitle=f"{expobj.t_series_name} - {expobj.exptype} - +ve sig. responders {title}",
                                    ylim=[-0.3, 0.8], fig=fig, ax=ax,
                                    pre_stim_sec=PhotostimAnalysisSlmTargets._pre_stim_sec,
                                    show=False, fontsize='small', figsize=(4, 4),
                                    xlabel='Time (secs)', ylabel='Avg. Stim. Response (dF/stdF)')
        else:
            print(f"**** {expobj.t_series_name} has no statistically significant positive responders.")
        if len(neg_avg_traces[0]) > 0:
            ax = axs if same_plot else axs[1]
            plot_periphotostim_avg2(dataset=neg_avg_traces, fps=expobj.fps,
                                    # legend_labels=[f"neg. cells: {len(neg_avg_traces[0])}"],
                                    colors=['blue'], avg_with_std=True,
                                    title=f"{expobj.t_series_name} - {expobj.exptype} - -ve sig. responders {title}",
                                    ylim=[-0.6, 0.5], fig=fig, ax=ax,
                                    pre_stim_sec=PhotostimAnalysisSlmTargets._pre_stim_sec,
                                    show=False, fontsize='small', figsize=(4, 4),
                                    xlabel='Time (secs)', ylabel='Avg. Stim. Response (dF/stdF)')
        else:
            print(f"**** {expobj.t_series_name} has no statistically significant negative responders.")

        if len(fake_avg_traces[0]) > 0:
            ax = axs if same_plot else None
            plot_periphotostim_avg2(dataset=fake_avg_traces, fps=expobj.fps,
                                    # legend_labels=[f"neg. cells: {len(neg_avg_traces[0])}"],
                                    colors=['black'], avg_with_std=True,
                                    title=f"{expobj.t_series_name} - {expobj.exptype}",
                                    ylim=[-0.6, 0.5], fig=fig, ax=ax,
                                    pre_stim_sec=PhotostimAnalysisSlmTargets._pre_stim_sec,
                                    show=False, fontsize='small', figsize=(4, 4),
                                    xlabel='Time (secs)', ylabel='Avg. Stim. Response (dF/stdF)')

        if same_plot:
            axs.set_xlim([-1, 2.5])

        fig.show()

    @staticmethod
    @Utils.run_for_loop_across_exps(run_pre4ap_trials=1, run_post4ap_trials=0, set_cache=0,
                                    skip_trials=PhotostimResponsesQuantificationNonTargets.EXCLUDE_TRIALS, )
    # run_trials=PhotostimResponsesQuantificationNonTargets.TEST_TRIALS)
    def run__plot_sig_responders_traces(plot_baseline_responders=False, **kwargs):
        """
        :param plot_baseline_responders: if True, for post-4ap exp, use the baseline responders' avgtraces for interictal and ictal groups
        :param kwargs:
        """
        expobj: Union[alloptical, Post4ap] = kwargs['expobj']
        if 'pre' in expobj.exptype:
            pos_avg_traces = [expobj.PhotostimResponsesNonTargets.pre4ap_possig_responders_avgtraces_baseline]
            neg_avg_traces = [expobj.PhotostimResponsesNonTargets.pre4ap_negsig_responders_avgtraces_baseline]
            fake_avg_traces = [np.mean(expobj.fakestims_dfstdF_traces_nontargets, axis=1)]
            expobj.PhotostimResponsesNonTargets.plot__pos_neg_responders_traces(expobj=expobj,
                                                                                pos_avg_traces=pos_avg_traces,
                                                                                neg_avg_traces=neg_avg_traces,
                                                                                fake_avg_traces=fake_avg_traces)

        elif 'post' in expobj.exptype:
            # INTERICTAL
            if plot_baseline_responders:
                pos_avg_traces = [
                    expobj.PhotostimResponsesNonTargets.post4ap_baseline_possig_responders_avgtraces_interictal]  # baseline responders
                neg_avg_traces = [
                    expobj.PhotostimResponsesNonTargets.post4ap_baseline_negsig_responders_avgtraces_interictal]  # baseline responders

            else:
                pos_avg_traces = [expobj.PhotostimResponsesNonTargets.post4ap_possig_responders_avgtraces_interictal]
                neg_avg_traces = [expobj.PhotostimResponsesNonTargets.post4ap_negsig_responders_avgtraces_interictal]

            expobj.PhotostimResponsesNonTargets.plot__pos_neg_responders_traces(expobj=expobj,
                                                                                pos_avg_traces=pos_avg_traces,
                                                                                neg_avg_traces=neg_avg_traces,
                                                                                title='interictal datapoints')

            # ICTAL
            if plot_baseline_responders:
                pos_avg_traces = [
                    expobj.PhotostimResponsesNonTargets.post4ap_baseline_possig_responders_avgtraces_ictal]  # baseline responders
                neg_avg_traces = [
                    expobj.PhotostimResponsesNonTargets.post4ap_baseline_negsig_responders_avgtraces_ictal]  # baseline responders

            else:
                pos_avg_traces = [
                    expobj.PhotostimResponsesNonTargets.post4ap_possig_responders_avgtraces_ictal]  # .post4ap_possig_responders_avgtraces_ictal not coded up yet
                neg_avg_traces = [
                    expobj.PhotostimResponsesNonTargets.post4ap_negsig_responders_avgtraces_ictal]  # .post4ap_negsig_responders_avgtraces_ictal not coded up yet

            expobj.PhotostimResponsesNonTargets.plot__pos_neg_responders_traces(expobj=expobj,
                                                                                pos_avg_traces=pos_avg_traces,
                                                                                neg_avg_traces=neg_avg_traces,
                                                                                title='outsz datapoints')

    # 2.2) PLOT -- BAR PLOT OF AVG MAGNITUDE OF RESPONSE
    @staticmethod
    def collect__avg_magnitude_response(results, collect_baseline_responders=False):
        """plot bar plot of avg magnitude of statistically significant responders across baseline and interictal, split up by positive and negative responders"""
        from _analysis_.nontargets_analysis._ClassResultsNontargetPhotostim import PhotostimResponsesNonTargetsResults
        results: PhotostimResponsesNonTargetsResults

        @Utils.run_for_loop_across_exps(run_pre4ap_trials=1, run_post4ap_trials=0, set_cache=0,
                                        skip_trials=PhotostimResponsesQuantificationNonTargets.EXCLUDE_TRIALS)
        def return__avg_magntiude_pos_response(**kwargs):
            """return avg magnitude of positive responders of stim trials -pre4ap """
            expobj: Union[alloptical, Post4ap] = kwargs['expobj']
            return np.mean(expobj.PhotostimResponsesNonTargets.pre4ap_possig_responders_responses)

        @Utils.run_for_loop_across_exps(run_pre4ap_trials=1, run_post4ap_trials=0, set_cache=0,
                                        skip_trials=PhotostimResponsesQuantificationNonTargets.EXCLUDE_TRIALS)
        def return__avg_magntiude_neg_response(**kwargs):
            """return avg magnitude of negitive responders of stim trials -pre4ap """
            expobj: Union[alloptical, Post4ap] = kwargs['expobj']
            return np.mean(expobj.PhotostimResponsesNonTargets.pre4ap_negsig_responders_responses)

        @Utils.run_for_loop_across_exps(run_pre4ap_trials=0, run_post4ap_trials=1, set_cache=0,
                                        skip_trials=PhotostimResponsesQuantificationNonTargets.EXCLUDE_TRIALS)
        def return__avg_magntiude_pos_response_interictal(**kwargs):
            """return avg magnitude of positive responders of stim trials - interictal"""
            expobj: Union[alloptical, Post4ap] = kwargs['expobj']
            if collect_baseline_responders:
                return np.mean(
                    expobj.PhotostimResponsesNonTargets.post4ap_baseline_possig_responders_responses_interictal)
            else:
                return np.mean(expobj.PhotostimResponsesNonTargets.post4ap_possig_responders_responses_interictal)

        @Utils.run_for_loop_across_exps(run_pre4ap_trials=0, run_post4ap_trials=1, set_cache=0,
                                        skip_trials=PhotostimResponsesQuantificationNonTargets.EXCLUDE_TRIALS)
        def return__avg_magntiude_neg_response_interictal(**kwargs):
            """return avg magnitude of negitive responders of stim trials - interictal"""
            expobj: Union[alloptical, Post4ap] = kwargs['expobj']
            if collect_baseline_responders:
                return np.mean(
                    expobj.PhotostimResponsesNonTargets.post4ap_baseline_negsig_responders_responses_interictal)
            else:
                return np.mean(expobj.PhotostimResponsesNonTargets.post4ap_negsig_responders_responses_interictal)

        @Utils.run_for_loop_across_exps(run_pre4ap_trials=0, run_post4ap_trials=1, set_cache=0,
                                        skip_trials=PhotostimResponsesQuantificationNonTargets.EXCLUDE_TRIALS)
        def return__avg_magntiude_pos_response_ictal(**kwargs):
            """return avg magnitude of positive responders of stim trials - ictal"""
            expobj: Union[alloptical, Post4ap] = kwargs['expobj']
            if collect_baseline_responders:
                return np.mean(expobj.PhotostimResponsesNonTargets.post4ap_baseline_possig_responders_responses_ictal)
            else:
                return np.mean(expobj.PhotostimResponsesNonTargets.post4ap_possig_responders_responses_ictal)

        @Utils.run_for_loop_across_exps(run_pre4ap_trials=0, run_post4ap_trials=1, set_cache=0,
                                        skip_trials=PhotostimResponsesQuantificationNonTargets.EXCLUDE_TRIALS)
        def return__avg_magntiude_neg_response_ictal(**kwargs):
            """return avg magnitude of negitive responders of stim trials - ictal"""
            expobj: Union[alloptical, Post4ap] = kwargs['expobj']
            if collect_baseline_responders:
                return np.mean(
                    expobj.PhotostimResponsesNonTargets.post4ap_baseline_negsig_responders_responses_ictal)
            else:
                return np.mean(expobj.PhotostimResponsesNonTargets.post4ap_negsig_responders_responses_ictal)

        pos_baseline = return__avg_magntiude_pos_response()
        neg_baseline = return__avg_magntiude_neg_response()
        pos_interictal = return__avg_magntiude_pos_response_interictal()
        neg_interictal = return__avg_magntiude_neg_response_interictal()
        pos_ictal = return__avg_magntiude_pos_response_ictal()
        neg_ictal = return__avg_magntiude_neg_response_ictal()

        if collect_baseline_responders:
            results.avg_baseline_responders_magnitude = {
                'baseline_positive': [val for i, val in enumerate(pos_baseline) if
                                      (not np.isnan(val) and not np.isnan(pos_interictal[i]))],
                'baseline_negative': [val for i, val in enumerate(neg_baseline) if
                                      (not np.isnan(val) and not np.isnan(neg_interictal[i]))],
                'interictal_positive': [val for i, val in enumerate(pos_interictal) if
                                        (not np.isnan(val) and not np.isnan(pos_baseline[i]))],
                'interictal_negative': [val for i, val in enumerate(neg_interictal) if
                                        (not np.isnan(val) and not np.isnan(neg_baseline[i]))],
                'ictal_positive': [val for i, val in enumerate(pos_ictal) if
                                   (not np.isnan(val) and not np.isnan(pos_baseline[i]))],
                'ictal_negative': [val for i, val in enumerate(neg_ictal) if
                                   (not np.isnan(val) and not np.isnan(neg_baseline[i]))]
            }

        else:
            results.avg_responders_magnitude = {'baseline_positive': [val for i, val in enumerate(pos_baseline) if (
                    not np.isnan(val) and not np.isnan(pos_interictal[i]))],
                                                'baseline_negative': [val for i, val in enumerate(neg_baseline) if (
                                                        not np.isnan(val) and not np.isnan(neg_interictal[i]))],
                                                'interictal_negative': [val for i, val in enumerate(neg_interictal) if (
                                                        not np.isnan(val) and not np.isnan(neg_baseline[i]))],
                                                'interictal_positive': [val for i, val in enumerate(pos_interictal) if (
                                                        not np.isnan(val) and not np.isnan(pos_baseline[i]))],
                                                'ictal_negative': [val for i, val in enumerate(neg_ictal) if (
                                                        not np.isnan(val) and not np.isnan(neg_baseline[i]))],
                                                'ictal_positive': [val for i, val in enumerate(pos_ictal) if (
                                                        not np.isnan(val) and not np.isnan(pos_baseline[i]))],
                                                }
        results.save_results()

    @staticmethod
    def plot__avg_magnitude_response(results, plot_baseline_responders=False):
        """plot bar plot of avg magnitude of statistically significant responders across baseline and interictal, split up by positive and negative responders
        :param results:
        :param plot_baseline_responders: if True, for post-4ap exp, use the baseline responders' avgtraces magnitude for interictal and ictal groups

        """
        from _analysis_.nontargets_analysis._ClassResultsNontargetPhotostim import PhotostimResponsesNonTargetsResults
        results: PhotostimResponsesNonTargetsResults

        if plot_baseline_responders:
            results_to_plot = results.avg_baseline_responders_magnitude
            title = ' - matched baseline responders'
        else:
            results_to_plot = results.avg_responders_magnitude
            title = '- within condition'

        pplot.plot_bar_with_points(data=[results_to_plot['baseline_positive'], results_to_plot['interictal_positive'],
                                         results_to_plot['ictal_positive']],
                                   paired=True, points=True, x_tick_labels=['baseline', 'interictal'],
                                   colors=['blue', 'green', 'purple'], y_label='Avg. magnitude of response',
                                   title='Positive responders' + title, bar=False, ylims=[-0.1, 1.0])

        pplot.plot_bar_with_points(data=[results_to_plot['baseline_negative'], results_to_plot['interictal_negative'],
                                         results_to_plot['ictal_negative']],
                                   paired=True, points=True, x_tick_labels=['baseline', 'interictal'],
                                   colors=['blue', 'green', 'purple'], y_label='Avg. magnitude of response',
                                   title='Negative responders' + title, bar=False, ylims=[-1.0, 0.1])

    # 2.3) PLOT -- BAR PLOT OF AVG TOTAL NUMBER OF POS. AND NEG RESPONSIVE CELLS
    @staticmethod
    def collect__avg_num_response(results):
        """
        collect: avg num of statistically significant responders across baseline and interictal, split up by positive and negative responders"""

        from _analysis_.nontargets_analysis._ClassResultsNontargetPhotostim import PhotostimResponsesNonTargetsResults
        results: PhotostimResponsesNonTargetsResults

        @Utils.run_for_loop_across_exps(run_pre4ap_trials=1, run_post4ap_trials=0, set_cache=0,
                                        skip_trials=PhotostimResponsesQuantificationNonTargets.EXCLUDE_TRIALS)
        def return__num_pos_responders(**kwargs):
            """return avg magnitude of positive responders of stim trials - pre4ap """
            expobj: Union[alloptical, Post4ap] = kwargs['expobj']
            return round(
                (expobj.PhotostimResponsesNonTargets.pre4ap_num_pos / len(expobj.s2p_nontargets_analysis)) * 100, 2)

        @Utils.run_for_loop_across_exps(run_pre4ap_trials=1, run_post4ap_trials=0, set_cache=0,
                                        skip_trials=PhotostimResponsesQuantificationNonTargets.EXCLUDE_TRIALS)
        def return__num_neg_responders(**kwargs):
            """return avg magnitude of negitive responders of stim trials - pre4ap """
            expobj: Union[alloptical, Post4ap] = kwargs['expobj']
            return round(
                (expobj.PhotostimResponsesNonTargets.pre4ap_num_neg / len(expobj.s2p_nontargets_analysis)) * 100, 2)

        @Utils.run_for_loop_across_exps(run_pre4ap_trials=0, run_post4ap_trials=1, set_cache=0,
                                        skip_trials=PhotostimResponsesQuantificationNonTargets.EXCLUDE_TRIALS)
        def return__num_pos_responders_interictal(**kwargs):
            """return avg magnitude of positive responders of stim trials - interictal"""
            expobj: Union[alloptical, Post4ap] = kwargs['expobj']
            return round((expobj.PhotostimResponsesNonTargets.post4ap_num_pos_interictal / len(
                expobj.s2p_nontargets_analysis)) * 100, 2)

        @Utils.run_for_loop_across_exps(run_pre4ap_trials=0, run_post4ap_trials=1, set_cache=0,
                                        skip_trials=PhotostimResponsesQuantificationNonTargets.EXCLUDE_TRIALS)
        def return__num_neg_responders_interictal(**kwargs):
            """return avg magnitude of negitive responders of stim trials - interictal"""
            expobj: Union[alloptical, Post4ap] = kwargs['expobj']
            return round((expobj.PhotostimResponsesNonTargets.post4ap_num_neg_interictal / len(
                expobj.s2p_nontargets_analysis)) * 100, 2)

        @Utils.run_for_loop_across_exps(run_pre4ap_trials=0, run_post4ap_trials=1, set_cache=0,
                                        skip_trials=PhotostimResponsesQuantificationNonTargets.EXCLUDE_TRIALS)
        def return__num_pos_responders_ictal(**kwargs):
            """return avg magnitude of positive responders of stim trials - ictal"""
            expobj: Union[alloptical, Post4ap] = kwargs['expobj']
            return round(
                (expobj.PhotostimResponsesNonTargets.post4ap_num_pos_ictal / len(expobj.s2p_nontargets_analysis)) * 100,
                2)

        @Utils.run_for_loop_across_exps(run_pre4ap_trials=0, run_post4ap_trials=1, set_cache=0,
                                        skip_trials=PhotostimResponsesQuantificationNonTargets.EXCLUDE_TRIALS)
        def return__num_neg_responders_ictal(**kwargs):
            """return avg magnitude of negitive responders of stim trials - ictal"""
            expobj: Union[alloptical, Post4ap] = kwargs['expobj']
            return round(
                (expobj.PhotostimResponsesNonTargets.post4ap_num_neg_ictal / len(expobj.s2p_nontargets_analysis)) * 100,
                2)

        pos_baseline = return__num_pos_responders()
        neg_baseline = return__num_neg_responders()
        pos_interictal = return__num_pos_responders_interictal()
        neg_interictal = return__num_neg_responders_interictal()
        pos_ictal = return__num_pos_responders_ictal()
        neg_ictal = return__num_neg_responders_ictal()

        results.avg_responders_num = {'baseline_positive': [val for i, val in enumerate(pos_baseline) if
                                                            (not np.isnan(val) and not np.isnan(pos_interictal[i]))],
                                      'baseline_negative': [val for i, val in enumerate(neg_baseline) if
                                                            (not np.isnan(val) and not np.isnan(neg_interictal[i]))],
                                      'interictal_positive': [val for i, val in enumerate(pos_interictal) if
                                                              (not np.isnan(val) and not np.isnan(pos_baseline[i]))],
                                      'interictal_negative': [val for i, val in enumerate(neg_interictal) if
                                                              (not np.isnan(val) and not np.isnan(neg_baseline[i]))],
                                      'ictal_positive': [val for i, val in enumerate(pos_ictal) if
                                                         (not np.isnan(val) and not np.isnan(pos_baseline[i]))],
                                      'ictal_negative': [val for i, val in enumerate(neg_ictal) if
                                                         (not np.isnan(val) and not np.isnan(neg_baseline[i]))]
                                      }
        results.save_results()

    @staticmethod
    def plot__avg_num_responders(results):
        """plot bar plot of avg number of statistically significant responders across baseline and interictal, split up by positive and negative responders"""
        from _analysis_.nontargets_analysis._ClassResultsNontargetPhotostim import PhotostimResponsesNonTargetsResults
        results: PhotostimResponsesNonTargetsResults

        pplot.plot_bar_with_points(
            data=[results.avg_responders_num['baseline_positive'], results.avg_responders_num['interictal_positive'],
                  results.avg_responders_num['ictal_positive']],
            paired=True, points=True, x_tick_labels=['baseline', 'interictal', 'ictal'],
            colors=['blue', 'green', 'purple'], y_label='Avg. responders (%)',
            title='Positive responders - within condition', bar=False, ylims=[0, 50])

        pplot.plot_bar_with_points(
            data=[results.avg_responders_num['baseline_negative'], results.avg_responders_num['interictal_negative'],
                  results.avg_responders_num['ictal_negative']],
            paired=True, points=True, x_tick_labels=['baseline', 'interictal', 'ictal'],
            colors=['blue', 'green', 'purple'], y_label='Avg. responders (%)',
            title='Negative responders - within condition', bar=False, ylims=[0, 50])

    # 3) ANALYSIS OF TOTAL EVOKED RESPONSES OF NETWORK #################################################################
    # 3.0) calculate - scatter plot of total evoked activity on trial vs. total activity of SLM targets on same trial - split up based on groups
    def _calculate__summed_responses(self, expobj: Union[alloptical, Post4ap]):
        """calculate total responses of all nontargets."""
        if 'pre' in self.expobj_exptype:
            # __positive_responders_responses = self.adata.X[self.adata.obs['positive_responder_baseline']] - leaving out for now.... there's a bunch of background work that needs to be done to figure this out with matching cells between pre4ap...post4ap...
            # summed_response_positive_baseline = list(np.sum(__positive_responders_responses,
            #                                                 axis=0))  #: summed response across all positive responders at each photostim trial

            # __negative_responders_responses = self.adata.X[self.adata.obs['negative_responder_baseline']] - leaving out for now.... there's a bunch of background work that needs to be done to figure this out with matching cells between pre4ap...post4ap...
            # summed_response_negative_baseline = list(np.sum(__negative_responders_responses,
            #                                                 axis=0))  #: summed response across all negative responders at each photostim trial

            network_summed_activity = list(
                np.sum(self.adata.X, axis=0))  #: summed responses across all nontargets at each photostim trial

            assert 'nontargets fakestim_responses' in self.adata.layers, 'nontargets fakestim_responses not found in adata layers'
            fakestims_network_summed_activity = list(np.sum(self.adata.layers['nontargets fakestim_responses'],
                                                            axis=0))  #: summed responses across all nontargets at each photostim trial

            # add as var to anndata
            # self.adata.add_variable(var_name='summed_response_pos_baseline', values=summed_response_positive_baseline)
            # self.adata.add_variable(var_name='summed_response_neg_baseline', values=summed_response_negative_baseline)
            self.adata.add_variable(var_name='total_nontargets_responses', values=network_summed_activity)
            self.adata.add_variable(var_name='total_nontargets_fakestims_responses',
                                    values=fakestims_network_summed_activity)

        elif 'post' in self.expobj_exptype:
            network_summed_activity = list(np.sum(self.adata.X, axis=0))

            assert 'nontargets fakestim_responses' in self.adata.layers, 'nontargets fakestim_responses not found in adata layers'
            fakestims_network_summed_activity = list(np.sum(self.adata.layers['nontargets fakestim_responses'],
                                                            axis=0))  #: summed responses across all nontargets at each photostim trial

            # interictal
            # __positive_responders_responses = self.adata.X[self.adata.obs['positive_responder_interictal']] - leaving out for now.... there's a bunch of background work that needs to be done to figure this out with matching cells between pre4ap...post4ap...
            # summed_response_positive_interictal = list(np.sum(__positive_responders_responses,
            #                                                   axis=0))  #: summed response across all positive responders at each photostim trial
            #
            # __negative_responders_responses = self.adata.X[self.adata.obs['negative_responder_interictal']] - leaving out for now.... there's a bunch of background work that needs to be done to figure this out with matching cells between pre4ap...post4ap...
            # summed_response_negative_interictal = list(np.sum(__negative_responders_responses,
            #                                                   axis=0))  #: summed response across all negative responders at each photostim trial

            fakestims_network_summed_activity_interictal = list(
                np.sum(self.adata.layers['nontargets fakestim_responses'][:, expobj.stim_idx_outsz],
                       axis=0))  #: summed responses across all nontargets at each photostim trial

            # ictal
            # __positive_responders_responses = self.adata.X[self.adata.obs['positive_responder_ictal']] - leaving out for now.... there's a bunch of background work that needs to be done to figure this out with matching cells between pre4ap...post4ap...
            # summed_response_positive_ictal = list(np.sum(__positive_responders_responses,
            #                                              axis=0))  #: summed response across all positive responders at each photostim trial
            #
            # __negative_responders_responses = self.adata.X[self.adata.obs['negative_responder_ictal']] - leaving out for now.... there's a bunch of background work that needs to be done to figure this out with matching cells between pre4ap...post4ap...
            # summed_response_negative_ictal = list(np.sum(__negative_responders_responses,
            #                                              axis=0))  #: summed response across all negative responders at each photostim trial

            fakestims_network_summed_activity_ictal = list(
                np.sum(self.adata.layers['nontargets fakestim_responses'][:, expobj.stim_idx_insz],
                       axis=0))  #: summed responses across all nontargets at each photostim trial

            # add as var to anndata
            self.adata.add_variable(var_name='total_nontargets_responses', values=network_summed_activity)
            self.adata.add_variable(var_name='total_nontargets_fakestims_responses',
                                    values=fakestims_network_summed_activity)

            # self.adata.add_variable(var_name='summed_response_pos_interictal',
            #                         values=summed_response_positive_interictal)
            # self.adata.add_variable(var_name='summed_response_neg_interictal',
            #                         values=summed_response_negative_interictal)

            # self.adata.add_variable(var_name='summed_response_pos_ictal', values=summed_response_positive_ictal)
            # self.adata.add_variable(var_name='summed_response_neg_ictal', values=summed_response_negative_ictal)

    def _calculate__mean_responses_nontargets(self, expobj: Union[alloptical, Post4ap]):
        """calculate total responses of significantly responding nontargets."""
        if 'pre' in self.expobj_exptype:
            network_mean_activity = list(
                np.mean(self.adata.X, axis=0))  #: mean responses across all nontargets at each photostim trial

            network_std_activity = list(
                np.std(self.adata.X, axis=0, ddof=1))  #: std of responses across all nontargets at each photostim trial

            assert 'nontargets fakestim_responses' in self.adata.layers, 'nontargets fakestim_responses not found in adata layers'
            fakestims_network_mean_activity = list(np.mean(self.adata.layers['nontargets fakestim_responses'],
                                                           axis=0))  #: summed responses across all nontargets at each photostim trial

            # add as var to anndata
            # self.adata.add_variable(var_name='summed_response_pos_baseline', values=summed_response_positive_baseline)
            # self.adata.add_variable(var_name='summed_response_neg_baseline', values=summed_response_negative_baseline)
            self.adata.add_variable(var_name='mean_nontargets_responses', values=network_mean_activity)
            self.adata.add_variable(var_name='std_nontargets_responses', values=network_std_activity)
            self.adata.add_variable(var_name='mean_nontargets_fakestims_responses',
                                    values=fakestims_network_mean_activity)

        elif 'post' in self.expobj_exptype:

            # all stims, all cells  ####################################################################################
            # network_mean_activity = list(np.mean(self.adata.X, axis=0))
            # network_std_activity = list(np.std(self.adata.X, axis=0, ddof=1))
            #
            # assert 'nontargets fakestim_responses' in self.adata.layers, 'nontargets fakestim_responses not found in adata layers'
            # fakestims_network_mean_activity = list(np.mean(self.adata.layers['nontargets fakestim_responses'],
            #                                                 axis=0))  #: summed responses across all nontargets at each photostim trial
            #
            # # add as var to anndata
            # self.adata.add_variable(var_name='mean_nontargets_responses', values=network_mean_activity)
            # self.adata.add_variable(var_name='std_nontargets_responses', values=network_std_activity)
            # self.adata.add_variable(var_name='mean_nontargets_fakestims_responses',
            #                         values=fakestims_network_mean_activity)

            # interictal ####################################################################################
            # __positive_responders_responses = self.adata.X[self.adata.obs['positive_responder_interictal']] - leaving out for now.... there's a bunch of background work that needs to be done to figure this out with matching cells between pre4ap...post4ap...
            # summed_response_positive_interictal = list(np.sum(__positive_responders_responses,
            #                                                   axis=0))  #: summed response across all positive responders at each photostim trial
            #
            # __negative_responders_responses = self.adata.X[self.adata.obs['negative_responder_interictal']] - leaving out for now.... there's a bunch of background work that needs to be done to figure this out with matching cells between pre4ap...post4ap...
            # summed_response_negative_interictal = list(np.sum(__negative_responders_responses,
            #                                                   axis=0))  #: summed response across all negative responders at each photostim trial

            # fakestims_network_mean_activity_interictal = list(
            #     np.mean(self.adata.layers['nontargets fakestim_responses'][:, expobj.stim_idx_outsz],
            #            axis=0))  #: summed responses across all nontargets at each photostim trial

            # ictal
            # __positive_responders_responses = self.adata.X[self.adata.obs['positive_responder_ictal']] - leaving out for now.... there's a bunch of background work that needs to be done to figure this out with matching cells between pre4ap...post4ap...
            # summed_response_positive_ictal = list(np.sum(__positive_responders_responses,
            #                                              axis=0))  #: summed response across all positive responders at each photostim trial
            #
            # __negative_responders_responses = self.adata.X[self.adata.obs['negative_responder_ictal']] - leaving out for now.... there's a bunch of background work that needs to be done to figure this out with matching cells between pre4ap...post4ap...
            # summed_response_negative_ictal = list(np.sum(__negative_responders_responses,
            #                                              axis=0))  #: summed response across all negative responders at each photostim trial

            # fakestims_network_mean_activity_ictal = list(
            #     np.mean(self.adata.layers['nontargets fakestim_responses'][:, expobj.stim_idx_insz],
            #            axis=0))  #: summed responses across all nontargets at each photostim trial

            # ICTAL - NONTARGET OUTSZ MEASUREMENTS #####################################################################
            outsz_mean_activity_stims = [None for i in range(self.adata.n_vars)]
            outsz_std_activity_stims = [None for i in range(self.adata.n_vars)]

            _cells_analyse = [cell for idx, cell in
                              enumerate(tuple(expobj.PhotostimResponsesNonTargets.adata.obs['original_index'])) if
                              cell in tuple(expobj.NonTargetsSzInvasionSpatial.adata.obs['original_index'])]
            _idx_analyse = [idx for idx, cell in
                            enumerate(tuple(expobj.PhotostimResponsesNonTargets.adata.obs['original_index'])) if
                            cell in tuple(expobj.NonTargetsSzInvasionSpatial.adata.obs['original_index'])]

            for i, stimidx in enumerate(expobj.stim_idx_insz):
                print(f'processing stim: {stimidx},  {len(expobj.stim_idx_insz)} total stims...')
                _outsz_cell_response = []
                for cell in _cells_analyse:
                    __idx = tuple(expobj.PhotostimResponsesNonTargets.adata.obs['original_index']).index(cell)
                    __jdx = tuple(expobj.NonTargetsSzInvasionSpatial.adata.obs['original_index']).index(cell)
                    if expobj.NonTargetsSzInvasionSpatial.adata.layers['in/out sz'][__jdx, stimidx] == 1:
                        response = expobj.PhotostimResponsesNonTargets.adata.X[__idx, stimidx]
                        _outsz_cell_response.append(response)
                if len(_outsz_cell_response) > 0:
                    outsz_mean_activity_stims[stimidx] = np.nanmean(_outsz_cell_response)
                    outsz_std_activity_stims[stimidx] = np.nanstd(_outsz_cell_response, ddof=1)

            self.adata.add_variable(var_name='mean_nontargets_responses - outsz', values=outsz_mean_activity_stims)
            self.adata.add_variable(var_name='std_nontargets_responses - outsz', values=outsz_std_activity_stims)

            # self.adata.add_variable(var_name='summed_response_pos_interictal',
            #                         values=summed_response_positive_interictal)
            # self.adata.add_variable(var_name='summed_response_neg_interictal',
            #                         values=summed_response_negative_interictal)

            # self.adata.add_variable(var_name='summed_response_pos_ictal', values=summed_response_positive_ictal)
            # self.adata.add_variable(var_name='summed_response_neg_ictal', values=summed_response_negative_ictal)

    def _calculate__summed_responses_targets(self, expobj: Union[alloptical, Post4ap]):
        """calculate total summed dFF responses of SLM targets of experiments to compare with summed responses of nontargets."""

        if 'pre' in self.expobj_exptype:
            summed_responses = list(np.sum(expobj.PhotostimResponsesSLMTargets.adata.X, axis=0))
            summed_fakestims_responses = list(
                np.sum(expobj.PhotostimResponsesSLMTargets.adata.layers['fakestim_responses'], axis=0))

            expobj.PhotostimResponsesSLMTargets.adata.add_variable(var_name='summed_response_SLMtargets',
                                                                   values=summed_responses)
            expobj.PhotostimResponsesSLMTargets.adata.add_variable(var_name='summed_fakestims_response_SLMtargets',
                                                                   values=summed_fakestims_responses)

            # return summed_responses

        elif 'post' in self.expobj_exptype:
            summed_responses = list(np.sum(expobj.PhotostimResponsesSLMTargets.adata.X, axis=0))
            summed_fakestims_responses = list(
                np.sum(expobj.PhotostimResponsesSLMTargets.adata.layers['fakestim_responses'], axis=0))

            expobj.PhotostimResponsesSLMTargets.adata.add_variable(var_name='summed_response_SLMtargets',
                                                                   values=summed_responses)
            expobj.PhotostimResponsesSLMTargets.adata.add_variable(var_name='summed_fakestims_response_SLMtargets',
                                                                   values=summed_fakestims_responses)

            # return summed_responses

        expobj.save()

    @staticmethod
    def run__summed_responses(rerun=0):
        @Utils.run_for_loop_across_exps(run_pre4ap_trials=0, run_post4ap_trials=1, allow_rerun=rerun,
                                        skip_trials=PhotostimResponsesQuantificationNonTargets.EXCLUDE_TRIALS, )
        # run_trials=PhotostimResponsesQuantificationNonTargets.TEST_TRIALS)
        def _run__summed_responses(**kwargs):
            expobj: Union[alloptical, Post4ap] = kwargs['expobj']
            # expobj.PhotostimResponsesNonTargets._calculate__summed_responses(expobj=expobj)
            # expobj.PhotostimResponsesNonTargets._calculate__summed_responses_targets(expobj=expobj)
            # assert 'summed_response_SLMtargets' in expobj.PhotostimResponsesSLMTargets.adata.var_keys(), 'summed responses SLM targets not saving in adata.var...'
            # assert 'summed_fakestims_response_SLMtargets' in expobj.PhotostimResponsesSLMTargets.adata.var_keys(), 'summed_fakestims_response_SLMtargets not saving in adata.var...'

            expobj.PhotostimResponsesNonTargets._calculate__mean_responses_nontargets(expobj=expobj)
            assert 'mean_nontargets_responses' in expobj.PhotostimResponsesNonTargets.adata.var_keys(), 'mean_nontargets_responses not saving in adata.var...'

            expobj.save()

        _run__summed_responses()

    # 3.1) plot - scatter plot of total nontargets evoked responses on trial vs. total responses of SLM targets on same trial - not zscored - individual trials, includes nontargets fakestims
    @staticmethod
    @Utils.run_for_loop_across_exps(run_pre4ap_trials=0, run_post4ap_trials=1, set_cache=0,
                                    skip_trials=FakeStimsQuantification.EXCLUDE_TRIALS + PhotostimResponsesQuantificationNonTargets.EXCLUDE_TRIALS, )
    # run_trials=PhotostimResponsesQuantificationNonTargets.TEST_TRIALS)
    def plot__exps_summed_nontargets_vs_summed_targets(**kwargs):
        expobj: Union[alloptical, Post4ap] = kwargs['expobj']

        self = expobj.PhotostimResponsesNonTargets
        if 'pre' in self.expobj_exptype:
            targets_responses_summed = expobj.PhotostimResponsesSLMTargets.adata.var['summed_response_SLMtargets']
            targets_fakestims_responses_summed = expobj.PhotostimResponsesSLMTargets.adata.var[
                'summed_fakestims_response_SLMtargets']
            nontargets_responses_summed = self.adata.var['total_nontargets_responses']
            nontargets_fakestims_responses_summed = self.adata.var['total_nontargets_fakestims_responses']
        elif 'post' in self.expobj_exptype:
            targets_responses_summed = expobj.PhotostimResponsesSLMTargets.adata.var['summed_response_SLMtargets'][
                expobj.stim_idx_outsz]
            targets_fakestims_responses_summed = \
                expobj.PhotostimResponsesSLMTargets.adata.var['summed_fakestims_response_SLMtargets'][
                    expobj.fake_stim_idx_outsz]
            nontargets_responses_summed = self.adata.var['total_nontargets_responses'][expobj.stim_idx_outsz]
            nontargets_fakestims_responses_summed = self.adata.var['total_nontargets_fakestims_responses'][
                expobj.fake_stim_idx_outsz]
        else:
            raise AttributeError()

        # fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(8, 8))
        # 
        # # photostim trials total targets vs. total non targets
        # slope, intercept, r_value, p_value, std_err = stats.linregress(x=targets_responses_summed,
        #                                                                y=nontargets_responses_summed)
        # regression_y = slope * targets_responses_summed + intercept
        # fig, axs[0] = pplot.make_general_scatter(x_list=[targets_responses_summed],
        #                                          y_data=[nontargets_responses_summed], figsize=(6.5, 4), fig=fig, ax=axs[0],
        #                                          s=50,facecolors=['orange'], edgecolors=['black'], lw=1, alpha=1,
        #                                          x_labels=['total targets activity (dFF summed)'], y_labels=['total network activity (dF/stdF summed)'],
        #                                          legend_labels=[f'photostim trials - $R^2$: {r_value ** 2:.2e}, p = {p_value**2:.2e}'], show=False)
        # axs[0].plot(targets_responses_summed, regression_y, color='black')
        # 
        # # fake stim trials
        # slope, intercept, r_value, p_value, std_err = stats.linregress(x=targets_fakestims_responses_summed,
        #                                                                y=nontargets_fakestims_responses_summed)
        # regression_y = slope * targets_fakestims_responses_summed + intercept
        # 
        # pplot.make_general_scatter(x_list = [targets_fakestims_responses_summed],
        #                            y_data=[nontargets_fakestims_responses_summed], s=50, facecolors=['gray'],
        #                            edgecolors=['black'], lw=1, alpha=1,
        #                            x_labels=['total targets activity (dFF summed)'], y_labels=['total network activity (dF/stdF summed)'],
        #                            fig = fig, ax= axs[1], legend_labels=[f'fakestim trials - $R^2$: {r_value**2:.2e}, p = {p_value**2:.2e}'], show = False)
        # axs[1].plot(targets_fakestims_responses_summed, regression_y, color = 'black')
        # 
        # axs[0].grid(True)
        # axs[1].grid(True)
        # fig.suptitle(f'Total responses for all trials {expobj.t_series_name}', wrap = True)
        # fig.tight_layout(pad=0.6)
        # fig.show()

        title = f'Total responses for all trials {expobj.t_series_name}'
        xlabel = 'total targets activity (dFF summed)'
        ylabel = 'total network activity (dF/stdF summed)'

        fig, axs = plt.subplots(figsize=(8, 4))

        # photostim trials total targets vs. total non targets
        slope, intercept, r_value, p_value, std_err = stats.linregress(x=targets_responses_summed,
                                                                       y=nontargets_responses_summed)
        photostimregression_y = slope * targets_responses_summed + intercept
        axs.scatter(targets_responses_summed, nontargets_responses_summed, color='orange', s=50,
                    label=f'photostim trials - $R^2$: {r_value ** 2:.2e}, p = {p_value ** 2:.2e}')

        # fake stim trials
        slope, intercept, r_value, p_value, std_err = stats.linregress(x=targets_fakestims_responses_summed,
                                                                       y=nontargets_fakestims_responses_summed)
        fakestimregression_y = slope * targets_fakestims_responses_summed + intercept
        axs.scatter(targets_fakestims_responses_summed, nontargets_fakestims_responses_summed, color='gray', s=50,
                    label=f'fakestim trials - $R^2$: {r_value ** 2:.2e}, p = {p_value ** 2:.2e}')

        axs.set_xlabel(xlabel)
        axs.set_ylabel(ylabel)
        axs.plot(targets_responses_summed, photostimregression_y, color='orange')
        axs.plot(targets_fakestims_responses_summed, fakestimregression_y, color='black')
        axs.grid(True)
        axs.grid(True)
        axs.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
        fig.suptitle(title, wrap=True)
        fig.tight_layout(pad=0.6)
        fig.show()

    # 3.2) plot - scatter plot of total evoked activity on trial vs. total activity of SLM targets on same trial - split up based on groups - z scored - all trials
    @staticmethod
    def collect__zscored_summed_activity_vs_targets_activity(results, rerun=1):
        from _analysis_.nontargets_analysis._ClassResultsNontargetPhotostim import PhotostimResponsesNonTargetsResults
        results: PhotostimResponsesNonTargetsResults

        # pre4ap - baseline
        @Utils.run_for_loop_across_exps(run_pre4ap_trials=True, run_post4ap_trials=False, allow_rerun=rerun,
                                        skip_trials=PhotostimResponsesQuantificationNonTargets.EXCLUDE_TRIALS)
        def collect_summed_responses_baseline(**kwargs):
            expobj: alloptical = kwargs['expobj']
            assert 'summed_response_SLMtargets' in expobj.PhotostimResponsesSLMTargets.adata.var_keys(), 'summed responses SLM targets not saving in adata.var...'
            assert 'summed_fakestims_response_SLMtargets' in expobj.PhotostimResponsesSLMTargets.adata.var_keys(), 'summed_fakestims_response_SLMtargets not saving in adata.var...'

            summed_responses = pd.DataFrame(
                {'exp': [expobj.t_series_name] * expobj.PhotostimResponsesSLMTargets.adata.n_vars,
                 'targets': expobj.PhotostimResponsesSLMTargets.adata.var['summed_response_SLMtargets'],
                 # 'targets_fakestims': expobj.PhotostimResponsesSLMTargets.adata.var['summed_fakestims_response_SLMtargets'],
                 # 'non-targets_pos': expobj.PhotostimResponsesNonTargets.adata.var['summed_response_pos_baseline'],
                 # 'non-targets_neg': expobj.PhotostimResponsesNonTargets.adata.var['summed_response_neg_baseline'],
                 'all_non-targets': expobj.PhotostimResponsesNonTargets.adata.var['total_nontargets_responses'],
                 # 'all_non-targets_fakestims': expobj.PhotostimResponsesNonTargets.adata.var['total_nontargets_fakestims_responses']
                 })

            summed_responses_fakestims = pd.DataFrame({
                'targets_fakestims': expobj.PhotostimResponsesSLMTargets.adata.var[
                    'summed_fakestims_response_SLMtargets'],
                'all_non-targets_fakestims': expobj.PhotostimResponsesNonTargets.adata.var[
                    'total_nontargets_fakestims_responses']
            })

            # z scoring of all collected responses
            network_summed_activity_zsco = np.round(stats.zscore(summed_responses['all_non-targets'], ddof=1), 3)
            targets_summed_activity_zsco = np.round(stats.zscore(summed_responses['targets'], ddof=1), 3)

            network_fakestims_summed_activity_zsco = np.round(
                stats.zscore(summed_responses_fakestims['all_non-targets_fakestims'], ddof=1), 3)
            targets_fakestims_summed_activity_zsco = np.round(
                stats.zscore(summed_responses_fakestims['targets_fakestims'], ddof=1), 3)

            # calculating linear regression metrics between summed targets and summed total network for each experiment

            # photostims - lin reg. stats
            slope, intercept, r_value, p_value, std_err = stats.linregress(x=targets_summed_activity_zsco,
                                                                           y=network_summed_activity_zsco)
            regression_y = slope * targets_summed_activity_zsco + intercept

            summed_responses['targets_summed_zscored'] = targets_summed_activity_zsco
            summed_responses['all_non-targets_zscored'] = network_summed_activity_zsco
            summed_responses['all_non-targets_score_regression'] = regression_y

            lin_reg_scores = pd.DataFrame({
                'exp': expobj.t_series_name,
                'slope': slope,
                'intercept': intercept,
                'r_value': r_value,
                'p_value': p_value,
                'mean_targets': np.mean(summed_responses['targets']),
                'mean_non-targets': np.mean(summed_responses['all_non-targets']),
                'std_targets': np.std(summed_responses['targets'], ddof=1),
                'std_non-targets': np.std(summed_responses['all_non-targets'], ddof=1),
                # 'mean_targets_fakestims': np.mean(summed_responses['targets_fakestims']),
                # 'mean_non-targets_fakestims': np.mean(summed_responses['all_non-targets_fakestims']),
                # 'std_targets_fakestims': np.std(summed_responses['targets_fakestims'], ddof=1),
                # 'std_non-targets_fakestims_': np.std(summed_responses['all_non-targets_fakestims'], ddof=1)
            }, index=[expobj.t_series_name])

            # fakestims - lin reg. stats
            slope, intercept, r_value, p_value, std_err = stats.linregress(x=targets_fakestims_summed_activity_zsco,
                                                                           y=network_fakestims_summed_activity_zsco)
            regression_y_fakestims = slope * targets_summed_activity_zsco + intercept

            summed_responses_fakestims['targets_fakestims_summed_zscored'] = targets_fakestims_summed_activity_zsco
            summed_responses_fakestims['all_non-targets_fakestims_zscored'] = network_fakestims_summed_activity_zsco
            summed_responses_fakestims['all_non-targets_fakestims_score_regression'] = regression_y_fakestims

            lin_reg_scores_fakestims = pd.DataFrame({
                'exp': expobj.t_series_name,
                'slope': slope,
                'intercept': intercept,
                'r_value': r_value,
                'p_value': p_value,
                'mean_targets_fakestims': np.mean(summed_responses_fakestims['targets_fakestims']),
                'mean_non-targets_fakestims': np.mean(summed_responses_fakestims['all_non-targets_fakestims']),
                'std_targets_fakestims': np.std(summed_responses_fakestims['targets_fakestims'], ddof=1),
                'std_non-targets_fakestims_': np.std(summed_responses_fakestims['all_non-targets_fakestims'], ddof=1)
            }, index=[expobj.t_series_name])

            return summed_responses, summed_responses_fakestims, lin_reg_scores, lin_reg_scores_fakestims
            # return expobj.PhotostimResponsesNonTargets.adata.var['summed_response_pos_baseline'], expobj.PhotostimResponsesSLMTargets.adata.var['summed_response_SLMtargets']

        func_collector_baseline = collect_summed_responses_baseline()

        if func_collector_baseline is not None:
            summed_responses_baseline = pd.DataFrame(
                {'exp': [], 'targets': [], 'non-targets_pos': [], 'non-targets_neg': [], 'all_non-targets': [],
                 'targets_summed_zscored': [], 'all_non-targets_zscored': [], 'all_non-targets_score_regression': []})

            summed_responses_fakestims = pd.DataFrame({})
            summed_responses_fakestims['targets_fakestims_summed_zscored'] = []
            summed_responses_fakestims['all_non-targets_fakestims_zscored'] = []
            summed_responses_fakestims['all_non-targets_fakestims_score_regression'] = []

            lin_reg_scores_baseline = pd.DataFrame(
                {'exp': [], 'slope': [], 'intercept': [], 'r_value': [], 'p_value': []})
            lin_reg_scores_fakestims = pd.DataFrame(
                {'exp': [], 'slope': [], 'intercept': [], 'r_value': [], 'p_value': []})

            for exp in func_collector_baseline:
                summed_responses_baseline = pd.concat([summed_responses_baseline, exp[0]])
                summed_responses_fakestims = pd.concat([summed_responses_fakestims, exp[1]])
                lin_reg_scores_baseline = pd.concat([lin_reg_scores_baseline, exp[2]])
                lin_reg_scores_fakestims = pd.concat([lin_reg_scores_fakestims, exp[3]])

            summed_responses_baseline.shape
            print('summed responses baseline shape', summed_responses_baseline.shape)

            results.summed_responses = {'baseline': summed_responses_baseline,
                                        'baseline - fakestims': summed_responses_fakestims}

            results.lin_reg_summed_responses = {'baseline': lin_reg_scores_baseline,
                                                'baseline - fakestims': lin_reg_scores_fakestims}

            results.save_results()

        # post4ap - interictal ####################################################################################################################################################################################################
        @Utils.run_for_loop_across_exps(run_pre4ap_trials=False, run_post4ap_trials=True, allow_rerun=rerun,
                                        skip_trials=PhotostimResponsesQuantificationNonTargets.EXCLUDE_TRIALS)
        def collect_summed_responses_interictal(lin_reg_scores, lin_reg_scores_fakestims, **kwargs):
            """collect z scored (to baseline) summed responses for fakestims - interictal. Exclude z scores > 5 or < -5"""
            expobj: Post4ap = kwargs['expobj']

            summed_responses = pd.DataFrame({'exp': [expobj.t_series_name] * sum(
                [expobj.PhotostimResponsesSLMTargets.adata.var['stim_group'] == 'interictal'][0]),
                                             'targets': expobj.PhotostimResponsesSLMTargets.adata.var[
                                                 'summed_response_SLMtargets'][
                                                 expobj.PhotostimResponsesSLMTargets.adata.var[
                                                     'stim_group'] == 'interictal'],
                                             # 'non-targets_pos': expobj.PhotostimResponsesNonTargets.adata.var['summed_response_pos_interictal'][expobj.PhotostimResponsesSLMTargets.adata.var['stim_group'] == 'interictal'],
                                             # 'non-targets_neg': expobj.PhotostimResponsesNonTargets.adata.var[
                                             #     'summed_response_neg_interictal'][
                                             #     expobj.PhotostimResponsesSLMTargets.adata.var[
                                             #         'stim_group'] == 'interictal'],
                                             'all_non-targets': expobj.PhotostimResponsesNonTargets.adata.var[
                                                 'total_nontargets_responses'][
                                                 expobj.PhotostimResponsesSLMTargets.adata.var[
                                                     'stim_group'] == 'interictal']
                                             })

            summed_responses_fakestims = {'targets_fakestims': expobj.PhotostimResponsesSLMTargets.adata.var[
                'summed_fakestims_response_SLMtargets'][expobj.fake_stim_idx_outsz],
                                          'all_non-targets_fakestims': expobj.PhotostimResponsesNonTargets.adata.var[
                                              'total_nontargets_fakestims_responses'][expobj.fake_stim_idx_outsz]
                                          }

            # # z scoring of all collected responses within condition
            # network_summed_activity_zsco = np.round(stats.zscore(summed_responses['all_non-targets'], ddof=1), 3)
            # targets_summed_activity_zsco = np.round(stats.zscore(summed_responses['targets'], ddof=1), 3)
            #
            # network_fakestims_summed_activity_zsco = np.round(stats.zscore(summed_responses_fakestims['all_non-targets_fakestims'], ddof=1), 3)
            # targets_fakestims_summed_activity_zsco = np.round(stats.zscore(summed_responses_fakestims['targets_fakestims'], ddof=1), 3)

            # z scoring to mean and std of BASELINE group of same experiment
            # find matched trial for post4ap
            from _exp_metainfo_.exp_metainfo import AllOpticalExpsToAnalyze
            for map_key, expid in AllOpticalExpsToAnalyze.trial_maps[
                'post'].items():  # find the pre4ap exp that matches with the current post4ap experiment
                if expobj.t_series_name in expid:
                    pre4ap_match_id = AllOpticalExpsToAnalyze.trial_maps['pre'][map_key]
                    if map_key == 'g':
                        pre4ap_match_id = AllOpticalExpsToAnalyze.trial_maps['pre'][map_key][1]
                    break

            # z scoring of responses to matched baseline - photostims
            network_summed_activity_zsco = np.round([(x - float(
                lin_reg_scores.loc[pre4ap_match_id, 'mean_non-targets'])) / float(
                lin_reg_scores.loc[pre4ap_match_id, 'std_non-targets']) for x in
                                                     list(summed_responses['all_non-targets'])], 3)
            targets_summed_activity_zsco = np.round([(x - float(
                lin_reg_scores.loc[pre4ap_match_id, 'mean_targets'])) / float(
                lin_reg_scores.loc[pre4ap_match_id, 'std_targets']) for x in list(summed_responses['targets'])], 3)

            # z scoring of responses to matched baseline - fakestims
            network_fakestims_summed_activity_zsco = np.round([(x - float(
                lin_reg_scores_fakestims.loc[pre4ap_match_id, 'mean_non-targets_fakestims'])) / float(
                lin_reg_scores_fakestims.loc[pre4ap_match_id, 'std_non-targets_fakestims_']) for x in list(
                summed_responses_fakestims['all_non-targets_fakestims'])], 3)
            targets_fakestims_summed_activity_zsco = np.round([(x - float(
                lin_reg_scores_fakestims.loc[pre4ap_match_id, 'mean_targets_fakestims'])) / float(
                lin_reg_scores_fakestims.loc[pre4ap_match_id, 'std_targets_fakestims']) for x in
                                                               list(summed_responses_fakestims['targets_fakestims'])],
                                                              3)

            # ------ exclude datapoints whose targets_summed_activity are >5 z score points (or < -5):
            include_idx = [idx for idx, zscore in enumerate(targets_summed_activity_zsco) if -5 < zscore < 5]
            if len(include_idx) < len(targets_summed_activity_zsco):
                print(
                    f'**** excluding {len(targets_summed_activity_zsco) - len(include_idx)} stims from exp: {expobj.t_series_name} ****')
            targets_summed_activity_zsco = np.array([targets_summed_activity_zsco[i] for i in include_idx])
            network_summed_activity_zsco = np.array([network_summed_activity_zsco[i] for i in include_idx])

            include_idx_fakestims = [idx for idx, zscore in enumerate(targets_fakestims_summed_activity_zsco) if
                                     -5 < zscore < 5]
            if len(include_idx_fakestims) < len(targets_fakestims_summed_activity_zsco):
                print(
                    f'**** excluding {len(targets_fakestims_summed_activity_zsco) - len(include_idx_fakestims)} fake stims from exp: {expobj.t_series_name} ****')

            targets_fakestims_summed_activity_zsco = np.array(
                [targets_fakestims_summed_activity_zsco[i] for i in include_idx_fakestims])
            network_fakestims_summed_activity_zsco = np.array(
                [network_fakestims_summed_activity_zsco[i] for i in include_idx_fakestims])

            # calculating linear regression metrics between summed targets and summed total network for each experiment
            # photostims
            slope, intercept, r_value, p_value, std_err = stats.linregress(x=targets_summed_activity_zsco,
                                                                           y=network_summed_activity_zsco)
            regression_y = slope * targets_summed_activity_zsco + intercept

            summed_responses_zscore = pd.DataFrame({'exp': [expobj.t_series_name] * len(regression_y),
                                                    'targets_summed_zscored': targets_summed_activity_zsco,
                                                    'all_non-targets_zscored': network_summed_activity_zsco,
                                                    'all_non-targets_score_regression': regression_y})

            lin_reg_scores = pd.DataFrame({
                'exp': expobj.t_series_name,
                'slope': slope,
                'intercept': intercept,
                'r_value': r_value,
                'p_value': p_value
            }, index=[expobj.t_series_name])

            # fakestims
            slope, intercept, r_value, p_value, std_err = stats.linregress(x=targets_fakestims_summed_activity_zsco,
                                                                           y=network_fakestims_summed_activity_zsco)
            regression_y_fakestims = slope * targets_fakestims_summed_activity_zsco + intercept

            summed_responses_fakestims_zscore = pd.DataFrame({})
            summed_responses_fakestims_zscore[
                'targets_fakestims_summed_zscored'] = targets_fakestims_summed_activity_zsco
            summed_responses_fakestims_zscore[
                'all_non-targets_fakestims_zscored'] = network_fakestims_summed_activity_zsco
            summed_responses_fakestims_zscore['all_non-targets_fakestims_score_regression'] = regression_y_fakestims

            lin_reg_scores_fakestims = pd.DataFrame({
                'exp': expobj.t_series_name,
                'slope': slope,
                'intercept': intercept,
                'r_value': r_value,
                'p_value': p_value
            }, index=[expobj.t_series_name])

            return summed_responses_zscore, summed_responses_fakestims_zscore, lin_reg_scores, lin_reg_scores_fakestims
            # return expobj.PhotostimResponsesNonTargets.adata.var['summed_response_pos_interictal'], expobj.PhotostimResponsesSLMTargets.adata.var['summed_response_SLMtargets']

        func_collector_interictal = collect_summed_responses_interictal(
            lin_reg_scores=results.lin_reg_summed_responses['baseline'],
            lin_reg_scores_fakestims=results.lin_reg_summed_responses['baseline - fakestims'])

        if func_collector_interictal is not None:

            # summed_responses_interictal = pd.DataFrame({'exp': [], 'targets': [], 'non-targets_pos': [], 'non-targets_neg': [], 'all_non-targets': [],
            #                                           'targets_summed_zscored': [], 'all_non-targets_zscored': [], 'all_non-targets_score_regression': []})

            summed_responses_interictal_zscore = pd.DataFrame({'exp': [],
                                                               'targets_summed_zscored': [],
                                                               'all_non-targets_zscored': [],
                                                               'all_non-targets_score_regression': [], })
            # 'targets_fakestims_summed_zscored': [], 'all_non-targets_fakestims_zscored': [], 'all_non-targets_fakestims_score_regression': []})

            summed_responses_fakestims_interictal_zscore = pd.DataFrame({})
            summed_responses_fakestims_interictal_zscore['targets_fakestims_summed_zscored'] = []
            summed_responses_fakestims_interictal_zscore['all_non-targets_fakestims_zscored'] = []
            summed_responses_fakestims_interictal_zscore['all_non-targets_fakestims_score_regression'] = []

            lin_reg_scores_interictal = pd.DataFrame(
                {'exp': [], 'slope': [], 'intercept': [], 'r_value': [], 'p_value': []})
            lin_reg_scores_fakestims_interictal = pd.DataFrame(
                {'exp': [], 'slope': [], 'intercept': [], 'r_value': [], 'p_value': []})

            for exp in func_collector_interictal:
                summed_responses_interictal_zscore = pd.concat([summed_responses_interictal_zscore, exp[0]])
                summed_responses_fakestims_interictal_zscore = pd.concat(
                    [summed_responses_fakestims_interictal_zscore, exp[1]])
                lin_reg_scores_interictal = pd.concat([lin_reg_scores_interictal, exp[2]])
                lin_reg_scores_fakestims_interictal = pd.concat([lin_reg_scores_fakestims_interictal, exp[3]])

            print('summed responses interictal zscore shape', summed_responses_interictal_zscore.shape)
            print('summed responses fakestims interictal zscore shape',
                  summed_responses_fakestims_interictal_zscore.shape)

            results.summed_responses['interictal'] = summed_responses_interictal_zscore
            results.summed_responses['interictal - fakestims'] = summed_responses_fakestims_interictal_zscore
            results.lin_reg_summed_responses['interictal'] = lin_reg_scores_interictal
            results.lin_reg_summed_responses['interictal - fakestims'] = lin_reg_scores_fakestims_interictal
            results.save_results()

    @staticmethod
    def plot__summed_activity_vs_targets_activity(results, fig=None, axs=None, **kwargs):
        """scatter plot of stim trials comparing zscored summed activity of targets and zscored summed activity of nontargets. during baseline and interictal. includes fakestims trial as well."""
        from _analysis_.nontargets_analysis._ClassResultsNontargetPhotostim import PhotostimResponsesNonTargetsResults
        results: PhotostimResponsesNonTargetsResults

        # make plots
        if axs is not None:
            assert len(axs) == 2
            axs_ = axs
        else:
            raise ValueError('axs arg must be a tuple.')
        # SCATTER PLOT OF DATAPOINTS
        fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(10, 7), dpi=500) if fig is None or axs is None else (
            fig, axs_)
        axs = axs[0]
        # BASELINE CONDITION

        # photostims
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            x=results.summed_responses['baseline']['targets_summed_zscored'],
            y=results.summed_responses['baseline']['all_non-targets_zscored'])
        regression_y = slope * results.summed_responses['baseline']['targets_summed_zscored'] + intercept
        axs[0].scatter(results.summed_responses['baseline']['targets_summed_zscored'],
                       results.summed_responses['baseline']['all_non-targets_zscored'],
                       facecolor='white', edgecolor=ExpMetainfo.figures.colors['baseline'], lw=0.5, alpha=1, s=5)

        print(f"\np(Baseline - photostims): {p_value:.2e}")
        print(f"m(Baseline - photostims): {slope:.2f}")
        print(f"R^2(Baseline - photostims): {r_value**2:.2f}")


        # pplot.make_general_scatter(
        #     x_list=[results.summed_responses['baseline']['targets_summed_zscored']],
        #     y_data=[results.summed_responses['baseline']['all_non-targets_zscored']], fig=fig, ax=axs[0], show=False,
        #     s=5, facecolors=['white'], edgecolors=['blue'], lw=1, alpha=1,
        #     x_labels=['total targets activity'], y_labels=['total network activity'])
        axs[0].plot(results.summed_responses['baseline']['targets_summed_zscored'], regression_y, color='blue', lw=1)
        # fig.show()

        # add fakestims
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            x=results.summed_responses['baseline - fakestims']['targets_fakestims_summed_zscored'],
            y=results.summed_responses['baseline - fakestims']['all_non-targets_fakestims_zscored'])
        regression_y = slope * results.summed_responses['baseline - fakestims'][
            'targets_fakestims_summed_zscored'] + intercept

        axs[0].scatter(results.summed_responses['baseline - fakestims']['targets_fakestims_summed_zscored'],
                       results.summed_responses['baseline - fakestims']['all_non-targets_fakestims_zscored'],
                       facecolor='white', edgecolor='black', lw=0.5, alpha=1, s=5)

        print(f"\np(Baseline - fakestims): {p_value:.2e}")
        print(f"m(Baseline - fakestims): {slope:.2f}")
        print(f"R^2(Baseline - fakestims): {r_value**2:.2f}")

        # pplot.make_general_scatter(
        #     x_list=[results.summed_responses['baseline - fakestims']['targets_fakestims_summed_zscored']],
        #     y_data=[results.summed_responses['baseline - fakestims']['all_non-targets_fakestims_zscored']],
        #     fig=fig, ax=axs[0],
        #     s=5, facecolors=['white'], edgecolors=['black'], lw=1, alpha=1,
        #     x_labels=['total targets'], y_labels=['total network activity'],
        #     legend_labels=[
        #         f'baseline - fakestims - $R^2$: {r_value ** 2:.2e}, p = {p_value ** 2:.2e}, $m$ = {slope:.2e}'],
        #     show=False)
        axs[0].plot(results.summed_responses['baseline - fakestims']['targets_fakestims_summed_zscored'], regression_y,
                    color='gray', lw=1)
        axs[0].set_ylabel('Total non-targets\nresponse (z-scored)', fontsize=10)



        # INTERICTAL CONDITION
        # TEST AND DEVELOP AND DEBU BELOW VERY NEXT!!!
        # photostims
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            x=results.summed_responses['interictal']['targets_summed_zscored'],
            y=results.summed_responses['interictal']['all_non-targets_zscored'])

        regression_y = slope * results.summed_responses['interictal']['targets_summed_zscored'] + intercept

        axs[1].scatter(results.summed_responses['interictal']['targets_summed_zscored'],
                       results.summed_responses['interictal']['all_non-targets_zscored'],
                       facecolor='white', edgecolor=ExpMetainfo.figures.colors['interictal'], lw=0.5, alpha=1, s=5)

        print(f"\np(Interictal - photostims): {p_value:.2e}")
        print(f"m(Interictal - photostims): {slope:.2f}")
        print(f"R^2(Interictal - photostims): {r_value**2:.2f}")

        # pplot.make_general_scatter(x_list=[results.summed_responses['interictal']['targets_summed_zscored']],
        #                            y_data=[results.summed_responses['interictal']['all_non-targets_zscored']], s=5,
        #                            facecolors=['white'],
        #                            edgecolors=['green'], lw=1, alpha=1, x_labels=['total targets activity'],
        #                            y_labels=['total network activity'], fig=fig, ax=axs[1],
        #                            legend_labels=[
        #                                f'interictal - photostims - $R^2$: {r_value ** 2:.2e}, p = {p_value ** 2:.2e}, $m$ = {slope:.2e}'],
        #                            show=False)

        axs[1].plot(results.summed_responses['interictal']['targets_summed_zscored'], regression_y, color='forestgreen',
                    lw=1)

        # fakestims
        # add fakestims
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            x=results.summed_responses['interictal - fakestims']['targets_fakestims_summed_zscored'],
            y=results.summed_responses['interictal - fakestims']['all_non-targets_fakestims_zscored'])
        regression_y = slope * results.summed_responses['interictal - fakestims'][
            'targets_fakestims_summed_zscored'] + intercept

        axs[1].scatter(results.summed_responses['interictal - fakestims']['targets_fakestims_summed_zscored'],
                       results.summed_responses['interictal - fakestims']['all_non-targets_fakestims_zscored'],
                       facecolor='white', edgecolor='black', lw=0.5, alpha=1, s=5)

        print(f"\np(Interictal - fakestims): {p_value:.2e}")
        print(f"m(Interictal - fakestims): {slope:.2f}")
        print(f"R^2(Interictal - fakestims): {r_value**2:.2f}")

        # pplot.make_general_scatter(
        #     x_list=[results.summed_responses['interictal - fakestims']['targets_fakestims_summed_zscored']],
        #     y_data=[results.summed_responses['interictal - fakestims']['all_non-targets_fakestims_zscored']],
        #     fig=fig, ax=axs[1],
        #     s=5, facecolors=['white'], edgecolors=['black'], lw=1, alpha=1,
        #     x_labels=['total targets'], y_labels=['total network activity'],
        #     legend_labels=[
        #         f'interictal - fakestims - $R^2$: {r_value ** 2:.2e}, p = {p_value ** 2:.2e}, $m$ = {slope:.2e}'],
        #     show=False)
        axs[1].plot(results.summed_responses['interictal - fakestims']['targets_fakestims_summed_zscored'],
                    regression_y, color='gray', lw=1)

        # PLOTTING OPTIONS
        # axs[0].grid(True)
        # axs[1].grid(True)
        axs[0].set_ylim([-15, 15])
        axs[1].set_ylim([-15, 15])
        axs[0].set_xlim([-7, 7])
        axs[1].set_xlim([-7, 7])
        axs[0].set_xticks([-5, 0, 5], [-5, 0, 5], fontsize=10)
        axs[1].set_xticks([-5, 0, 5], [-5, 0, 5], fontsize=10)
        # axs[0].set_xticklabels([])
        # axs[0].set_yticks([-5, 0, 5])
        axs[0].set_yticks([-10, 0, 10], [-10, 0, 10], fontsize=10)
        axs[1].set_yticklabels([])
        # axs[0].set_xlabel(f'Total targets response\n' + r'($\it{z}$-scored)', ha='center')
        # axs[1].set_ylabel(f'Total nontargets response\n' + r'($\it{z}$-scored)', ha='center')

        # fig.suptitle('Total z-scored (to baseline) responses for all trials, all exps', wrap=True)
        # fig.tight_layout(pad=0.6)
        # fig.show()

        SAVE_FOLDER = kwargs['SAVE_FOLDER']
        # Utils.save_figure(fig=fig, save_path_full=f'{SAVE_FOLDER}/total_targets_vs_total_nontargets_photostim_fakestim_baseline_interictal.png')

        # BAR PLOT OF PEARSON'S R CORR VALUES BETWEEN BASELINE AND INTERICTAL, AND SLOPE OF REGRESSION
        axs = axs_[1]

        # STATS TESTS:
        r2_ratio_baseline = [(val ** 2) / results.lin_reg_summed_responses['baseline - fakestims']['r_value'][i] for
                             i, val in enumerate(results.lin_reg_summed_responses['baseline']['r_value'])]
        r2_ratio_interictal = [(val ** 2) / results.lin_reg_summed_responses['interictal - fakestims']['r_value'][i] for
                               i, val in enumerate(results.lin_reg_summed_responses['interictal']['r_value'])]

        print(f"\nP(ttest rel of r2 photostim/fakestim ratio): {stats.ttest_rel(r2_ratio_baseline, r2_ratio_interictal)[1]}")
        print(f"P(ttest rel of r2 photostim/fakestim ratio): {stats.ttest_rel(r2_ratio_baseline, r2_ratio_interictal)[1]}")
        print(f"P(wilcoxon of r2 photostim/fakestim ratio): {stats.wilcoxon(r2_ratio_baseline, r2_ratio_interictal)[1]}")
        print(f"P(wilcoxon of r2 photostim/fakestim ratio - baseline != 1): {stats.wilcoxon(r2_ratio_baseline, [1] * len(r2_ratio_baseline))[1]}")
        print(f"P(wilcoxon of r2 photostim/fakestim ratio - interictal != 1): {stats.wilcoxon(r2_ratio_interictal, [1] * len(r2_ratio_interictal))[1]}")

        # MAKE PLOT
        fig, ax = pplot.plot_bar_with_points(data=[r2_ratio_baseline, r2_ratio_interictal],
                                             paired=True, bar=False, colors=[ExpMetainfo.figures.colors['baseline'], ExpMetainfo.figures.colors['interictal']],
                                             edgecolor='black', lw=1, s=25, alpha=1, shrink_text=0.8,
                                             x_tick_labels=['Base', 'Inter'], ylims=[0, 1.5], title='$R^2$',
                                             y_ticklabels=[0, 0.5, 1.0, 1.5],y_label='Ratio',
                                             # title='ratio of $R^2$ per experiment',
                                             fig=fig, ax=axs[0], show=False, capsize=0.7, fontsize=10)
        ax.spines['bottom'].set_visible(False)
        ax.set_xticks([])
        # fig.tight_layout(pad=0.5)
        # fig.show()
        # Utils.save_figure(fig=fig, save_path_full=f'{SAVE_FOLDER}/targets_nontargets_r2_ratio_photostim_fakestim.png')

        # BAR PLOT OF LINEAR REGRESSION SLOPE VALUES BETWEEN BASELINE AND INTERICTAL

        # STATS TESTS:
        m_ratio_baseline = [val / results.lin_reg_summed_responses['baseline - fakestims']['slope'][i] for i, val in
                            enumerate(results.lin_reg_summed_responses['baseline']['slope'])]
        m_ratio_interictal = [val / results.lin_reg_summed_responses['interictal - fakestims']['slope'][i] for i, val in
                              enumerate(results.lin_reg_summed_responses['interictal']['slope'])]

        print(f"\nP(ttest rel of m photostim/fakestim ratio): {stats.ttest_rel(m_ratio_baseline, m_ratio_interictal)[1]}")
        print(f"P(ttest ind of m photostim/fakestim ratio): {stats.ttest_ind(m_ratio_baseline, m_ratio_interictal)[1]}")
        print(f"P(wilcoxon of m photostim/fakestim ratio): {stats.wilcoxon(m_ratio_baseline, m_ratio_interictal)[1]}")
        print(f"P(wilcoxon of m photostim/fakestim ratio - baseline != 1): {stats.wilcoxon(m_ratio_baseline, [1] * len(m_ratio_baseline))[1]}")
        print(f"P(wilcoxon of m photostim/fakestim ratio - interictal != 1): {stats.wilcoxon(m_ratio_interictal, [1] * len(m_ratio_interictal))[1]}")

        # MAKE PLOT
        fig, ax = pplot.plot_bar_with_points(data=[m_ratio_baseline, m_ratio_interictal],
                                             paired=True, bar=False, colors=[ExpMetainfo.figures.colors['baseline'], ExpMetainfo.figures.colors['interictal']],
                                             edgecolor='black', lw=1, s=25, alpha=1,
                                             shrink_text=0.8,
                                             x_tick_labels=['Base', 'Inter'], ylims=[0, 4],
                                             y_ticklabels=[0, 1, 2, 3, 4], title='Slope', y_label='',
                                             # title='ratio of $m$ per experiment',
                                             fig=fig, ax=axs[1], show=False, capsize=0.7, fontsize=10)
        ax.spines['bottom'].set_visible(False)
        ax.set_xticks([])

        # fig.tight_layout(pad=0.5)
        # fig.show()
        # Utils.save_figure(fig=fig, save_path_full=f'{SAVE_FOLDER}/targets_nontargets_slope_ratio_photostim_fakestim.png')

        # pplot.plot_bar_with_points(data=[[i ** 2 for i in results.lin_reg_summed_responses['baseline']['r_value']],
        #                                  [i ** 2 for i in
        #                                   results.lin_reg_summed_responses['baseline - fakestims']['r_value']],
        #                                  [i ** 2 for i in results.lin_reg_summed_responses['interictal']['r_value']],
        #                                  [i ** 2 for i in
        #                                   results.lin_reg_summed_responses['interictal - fakestims']['r_value']]],
        #                            paired=True, bar=False, colors=['royalblue', 'skyblue', 'seagreen', 'lightgreen'], edgecolor='black',
        #                            lw=1, s=30, alpha=1, shrink_text=1.5,
        #                            x_tick_labels=['Base', 'Base-fake', 'Inter', 'Inter-fake'], ylims=[0, 1],
        #                            y_label='$R^2$', title='$R^2$ value per experiment')
        #
        # pplot.plot_bar_with_points(data=[[i for i in results.lin_reg_summed_responses['baseline']['slope']],
        #                                  [i for i in results.lin_reg_summed_responses['baseline - fakestims']['slope']],
        #                                  [i for i in results.lin_reg_summed_responses['interictal']['slope']],
        #                                  [i for i in
        #                                   results.lin_reg_summed_responses['interictal - fakestims']['slope']]],
        #                            paired=True, bar=False, colors=['royalblue', 'skyblue', 'seagreen', 'lightgreen'], edgecolor='black',
        #                            lw=1, s=50, alpha=1, shrink_text=1.5,
        #                            x_tick_labels=['Base', 'Base-fake', 'Inter', 'Inter-fake'], ylims=[0, 1.7],
        #                            y_label='$slope$', title='slope value per experiment')

        pass


if __name__ == '__main__':
    # expobj: alloptical = Utils.import_expobj(exp_prep='RL108 t-009')
    # expobj: Post4ap = Utils.import_expobj(exp_prep='RL108 t-013')

    pass
