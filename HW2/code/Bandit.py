"""
  Run this file at first, in order to see what is it printng. Instead of the print() use the respective log level
"""
############################### LOGGER
from abc import ABC, abstractmethod
import numpy as np
from loguru import logger
import csv
from pathlib import Path
import matplotlib.pyplot as plt




class Bandit(ABC):
    ##==== DO NOT REMOVE ANYTHING FROM THIS CLASS ====##

    @abstractmethod
    def __init__(self, p):
        pass

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def pull(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def experiment(self):
        pass

    @abstractmethod
    def report(self):
        # store data in csv
        # print average reward (use f strings to make it informative)
        # print average regret (use f strings to make it informative)
        pass

#--------------------------------------#





class Visualization:

    """Make plots that show what the two algorithms learned and earned.

    The class uses finished experiments, so it never changes how bandits
    are chosen or how rewards are generated.
    """
    def __init__(self, eg, ts):

        """Keep both experiments and choose where to save the graphs.

        Args:
            eg: Epsilon-Greedy experiment after it has finished running.
            ts: Thompson Sampling experiment after it has finished running.
        """
        self.eg = eg  # Keep the Epsilon-Greedy results for the plots.
        self.ts = ts  # Keep the Thompson Sampling results too.

        self.output_dir = (Path(__file__).resolve().parent / "outputs")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _learning_history(self, experiment):


        """Rebuild the mean estimate for every bandit after every trial.

        The experiments save rewards and selected bandits, but not all the
        intermediate estimates. We go through the observations in order
        and calculate those estimates again for plotting.

        Epsilon-Greedy uses the average observed reward. Thompson Sampling
        uses its Gaussian posterior mean, combining the prior with the
        rewards observed so far.

        Args:
            experiment: The completed Epsilon-Greedy or Thompson experiment.

        Returns:
            numpy.ndarray: One row per trial and one column per bandit.
        """
        n_trials = len(experiment.rewards)
        n_bandits = len(experiment.bandits)

        history = np.zeros((n_trials, n_bandits))  # One row per trial, one column per bandit.
        counts = np.zeros(n_bandits, dtype=int)
        reward_sums = np.zeros(n_bandits)

        for t in range(n_trials):
            j = experiment.selected_bandits[t]
            reward = experiment.rewards[t]

            counts[j] += 1
            reward_sums[j] += reward

            for k in range(n_bandits):

                if isinstance(experiment, ThompsonSampling):
                    # Rebuild the posterior mean from the prior and rewards seen so far.
                    bandit = experiment.bandits[k]

                    prior_precision = bandit.prior_precision
                    prior_mean = bandit.prior_mean
                    reward_precision = bandit.reward_precision

                    history[t, k] = (
                        prior_precision * prior_mean
                        + reward_precision * reward_sums[k]
                    ) / (
                        prior_precision
                        + reward_precision * counts[k]
                    )

                else:
                    # Epsilon-Greedy learns from the average reward observed so far.
                    if counts[k] > 0:
                        history[t, k] = (
                            reward_sums[k] / counts[k]
                        )

        return history

    def plot1(self):


        """Save the learning plots for both algorithms.

        Each figure has two views of the same data: a regular trial axis
        and a logarithmic trial axis. The log view makes it easier to see
        what happened during the first few trials. Dotted horizontal lines
        show each bandit's true mean for reference.
        """
        experiments = [
            (self.eg, "Epsilon-Greedy", "epsilon_greedy"),
            (self.ts, "Thompson Sampling", "thompson_sampling")
        ]

        for experiment, title, filename in experiments:

            history = self._learning_history(experiment)
            trials = np.arange(1, len(history) + 1)

            fig, axes = plt.subplots(
                1, 2, figsize=(14, 5)
            )

            for j, bandit in enumerate(experiment.bandits):

                label = f"Bandit {j + 1}"

                # Linear-scale plot
                axes[0].plot(
                    trials,
                    history[:, j],
                    label=label
                )

                # Logarithmic trial-axis plot
                axes[1].plot(
                    trials,
                    history[:, j],
                    label=label
                )

                # True expected reward reference lines
                axes[0].axhline(
                    y=bandit.p,
                    linestyle=":",
                    alpha=0.35
                )

                axes[1].axhline(
                    y=bandit.p,
                    linestyle=":",
                    alpha=0.35
                )

            axes[0].set_title("Linear Scale")
            axes[1].set_title("Logarithmic Scale")
            axes[1].set_xscale("log")

            for ax in axes:
                ax.set_xlabel("Trial Number")
                ax.set_ylabel("Estimated Mean Reward")
                ax.grid(True, alpha=0.3)
                ax.legend()

            fig.suptitle(
                f"{title}: Learning Process",
                fontsize=14
            )

            fig.tight_layout()

            save_path = (
                self.output_dir / f"{filename}_learning.png"
            )

            fig.savefig(
                save_path,
                dpi=300,
                bbox_inches="tight"
            )

            plt.close(fig)

            logger.info(f"Learning plot saved: {save_path}")

    def plot2(self):


        # Ensure reports have calculated cumulative arrays
        """Save graphs comparing total reward and regret over time.

        Higher cumulative reward is better. Lower cumulative pseudo-regret
        is better, because it means we spent fewer trials on weaker bandits.
        """
        for experiment in [self.eg, self.ts]:
            if not hasattr(experiment, "cumulative_rewards"):
                experiment.report()

        trials = np.arange(1, len(self.eg.rewards) + 1)

        # Figure 3: Cumulative rewards
        fig, ax = plt.subplots(figsize=(10, 6))

        ax.plot(
            trials,
            self.eg.cumulative_rewards,
            label="Epsilon-Greedy"
        )

        ax.plot(
            trials,
            self.ts.cumulative_rewards,
            label="Thompson Sampling"
        )

        ax.set_title("Cumulative Reward Comparison")
        ax.set_xlabel("Trial Number")
        ax.set_ylabel("Cumulative Reward")
        ax.legend()
        ax.grid(True, alpha=0.3)

        fig.tight_layout()

        reward_path = (
            self.output_dir / "cumulative_rewards.png"
        )

        fig.savefig(
            reward_path, dpi=300, bbox_inches="tight"
        )
        plt.close(fig)

        logger.info(f"Reward plot saved: {reward_path}")

        # Figure 4: Cumulative regrets
        fig, ax = plt.subplots(figsize=(10, 6))

        ax.plot(
            trials,
            self.eg.cumulative_regrets,
            label="Epsilon-Greedy"
        )

        ax.plot(
            trials,
            self.ts.cumulative_regrets,
            label="Thompson Sampling"
        )

        ax.set_title("Cumulative Pseudo-Regret Comparison")
        ax.set_xlabel("Trial Number")
        ax.set_ylabel("Cumulative Pseudo-Regret")
        ax.legend()
        ax.grid(True, alpha=0.3)

        fig.tight_layout()

        regret_path = (
            self.output_dir / "cumulative_regrets.png"
        )

        fig.savefig(
            regret_path, dpi=300, bbox_inches="tight"
        )
        plt.close(fig)

        logger.info(f"Regret plot saved: {regret_path}")


#--------------------------------------#

class EpsilonGreedy(Bandit):
    """Learn which bandit pays best using occasional random exploration.

    This algorithm usually chooses the highest estimated mean reward.
    With probability epsilon = 1 / trial_number, it explores by choosing
    a random bandit instead.
    """
    def __init__(self, p):
        """Start a bandit with a true mean and no observations.

        Args:
            p (float): True mean reward, used only to simulate rewards.
                The selection rule must use p_estimate instead of p.
        """
        self.p = p  # The true mean used when generating example rewards.
        self.p_estimate = 0.0  # Our starting guess before seeing any reward.
        self.N = 0  # How many times we have played this bandit.

    def __repr__(self):
        """Return a short description of this bandit."""
        return f"EpsilonGreedy Bandit (true mean={self.p})"

    def pull(self):
        """Simulate one play and return its random reward.

        Returns:
            float: A reward drawn from a normal distribution with mean p
                and standard deviation 1.
        """
        return np.random.normal(loc=self.p, scale=1.0)

    def update(self, x):
        """Update our estimate after receiving one new reward.

        We use the running-average formula. This gives the same answer as
        averaging every reward again, without keeping the whole history.

        Args:
            x (float): Reward received from this bandit.
        """
        self.N += 1
        self.p_estimate += (x - self.p_estimate) / self.N


    def experiment(self):
        """Run Epsilon-Greedy for 20,000 trials on four bandits.

        Epsilon starts at 1 and shrinks as 1/t. Exploration picks a random
        bandit; exploitation picks the one with the highest mean estimate.
        After each choice, we save the reward and update that bandit.

        Returns:
            numpy.ndarray: The reward received on each of the 20,000 trials.
        """
        Bandit_Reward = [1, 2, 3, 4]
        NumberOfTrials = 20000

        bandits = [EpsilonGreedy(p) for p in Bandit_Reward]  # One object for each advertisement.

        rewards = np.zeros(NumberOfTrials)  # One reward per trial.
        selected_bandits = np.zeros(NumberOfTrials, dtype=int)

        num_explored = 0
        num_exploited = 0

        for t in range(1, NumberOfTrials + 1):

            epsilon = 1 / t

            if np.random.random() < epsilon:  # Explore: try a random bandit.
                j = np.random.randint(len(bandits))
                num_explored += 1
            else:
                j = np.argmax([b.p_estimate for b in bandits])  # Exploit: trust the best estimate.
                num_exploited += 1


            reward = bandits[j].pull()  # See what reward we actually receive.
            bandits[j].update(reward)  # Learn from this new observation.
            rewards[t - 1] = reward  # Save the reward for later analysis.
            selected_bandits[t - 1] = j

       # Keep these results so reporting and plotting can use them.
        self.bandits = bandits
        self.rewards = rewards
        self.selected_bandits = selected_bandits
        self.num_explored = num_explored
        self.num_exploited = num_exploited

        logger.info("Epsilon-Greedy experiment completed.")

        return rewards


    def report(self):
        """Calculate results, save the CSV, and log a short summary.

        Cumulative reward is the total of the actual rewards. Pseudo-regret
        uses the difference between the best true mean and the true mean
        of the chosen bandit, so random reward noise does not count as a
        wrong decision.

        Returns:
            dict: Total and average reward, total and average pseudo-regret,
                and the path to this algorithm's CSV file.

        Raises:
            RuntimeError: If the experiment has not run yet.
        """
        if not hasattr(self, "rewards"):
            raise RuntimeError(
                "Run experiment() before report()."
            )


        self.cumulative_rewards = np.cumsum(self.rewards)  # Running total of actual rewards.
        total_reward = self.cumulative_rewards[-1]
        average_reward = np.mean(self.rewards)  # Mean reward per trial.
        optimal_mean = max(b.p for b in self.bandits)

        chosen_means = np.array([
            self.bandits[j].p for j in self.selected_bandits
        ])

        instant_regret = optimal_mean - chosen_means  # Expected loss from each choice.
        self.cumulative_regrets = np.cumsum(instant_regret)

        total_regret = self.cumulative_regrets[-1]
        average_regret = np.mean(instant_regret)


        output_dir = Path(__file__).resolve().parent / "outputs"
        output_dir.mkdir(parents=True, exist_ok=True)

        csv_path = output_dir / "epsilon_greedy_rewards.csv"  # Save this algorithm separately.

        with open(csv_path, "w", newline="") as file:
            writer = csv.writer(file)

            writer.writerow(["Bandit", "Reward", "Algorithm"])

            for j, reward in zip(self.selected_bandits, self.rewards):
                writer.writerow([
                    int(j) + 1,
                    float(reward),
                    "EpsilonGreedy"
                ])


        logger.info("===== Epsilon-Greedy Report =====")
        logger.info(f"Total trials: {len(self.rewards)}")
        logger.info(f"Cumulative reward: {total_reward:.2f}")
        logger.info(f"Average reward: {average_reward:.4f}")
        logger.info(f"Cumulative regret: {total_regret:.2f}")
        logger.info(f"Average regret: {average_regret:.4f}")
        logger.info(f"Explorations: {self.num_explored}")
        logger.info(f"Exploitations: {self.num_exploited}")

        logger.info(f"Rewards saved to: {csv_path}")

        return {
            "total_reward": total_reward,
            "average_reward": average_reward,
            "cumulative_regret": total_regret,
            "average_regret": average_regret,
            "csv_path": csv_path
        }


#--------------------------------------#


class ThompsonSampling(Bandit):

    """Choose bandits by sampling from uncertain beliefs about reward.

    Each bandit starts with a normal prior for its unknown mean. Rewards
    are normal with known precision. New rewards update the posterior;
    sampling from that posterior balances learning and earning.
    """
    def __init__(self, p):
        """Set up the true reward distribution and our initial belief.

        Args:
            p (float): True mean reward used to generate observations.
                The algorithm does not use it to decide which bandit wins.

        The reward precision is 1 (so reward variance is 1). The prior
        has mean 0 and precision 0.1 (so prior variance is 10).
        """
        self.p = p
        self.reward_precision = 1.0
        self.prior_mean = 0.0
        self.prior_precision = 0.1

        self.posterior_mean = self.prior_mean
        self.posterior_precision = self.prior_precision

        self.N = 0

    def __repr__(self):
        """Return a short description of this bandit."""
        return (
            f"ThompsonSampling Bandit "
            f"(true mean={self.p})"
        )

    def pull(self):

        """Generate one actual reward from this band's normal distribution.

        Returns:
            float: A Gaussian reward centered on the true mean p.
        """
        reward_std = np.sqrt(1 / self.reward_precision)

        return np.random.normal(loc=self.p, scale=reward_std)  # Actual observed reward.

    def sample(self):

        """Draw a possible mean from what we currently believe.

        This is not an observed reward. It is a sample from the posterior
        distribution of the unknown mean, used to decide which bandit to try.

        Returns:
            float: One random sample from the current normal posterior.
        """
        posterior_std = np.sqrt(1 / self.posterior_precision)

        return np.random.normal(loc=self.posterior_mean, scale=posterior_std)  # Our sampled belief, not a reward.

    def update(self, x):
        # Combine our previous belief with the reward we just saw.
        """Update the normal posterior using one observed reward.

        We add the known reward precision to the current precision,
        then calculate a new mean that weighs our old belief and the
        observation by their precisions. More observations make the
        posterior narrower, so we become more certain.

        Args:
            x (float): Actual reward observed after playing this bandit.
        """
        old_precision = self.posterior_precision
        old_mean = self.posterior_mean

        self.posterior_precision = (
            old_precision + self.reward_precision
        )

        self.posterior_mean = (
            old_precision * old_mean
            + self.reward_precision * x
        ) / self.posterior_precision

        self.N += 1

    def experiment(self):
        """Run 20,000 trials of Gaussian Thompson Sampling.

        Each trial samples one possible mean from each band's posterior,
        selects the highest sample, observes its reward, and updates only
        that bandit's posterior. The choices and rewards are saved.

        Returns:
            numpy.ndarray: The reward received on each trial.
        """
        Bandit_Reward = [1, 2, 3, 4]
        NumberOfTrials = 20000

        bandits = [ThompsonSampling(p) for p in Bandit_Reward]  # Four separate beliefs.

        rewards = np.zeros(NumberOfTrials)  # Keep each trial's reward.
        selected_bandits = np.zeros(NumberOfTrials, dtype=int)

        for t in range(NumberOfTrials):

            samples = [b.sample() for b in bandits]  # Draw one possible mean for each bandit.

            j = np.argmax(samples)  # Choose the highest posterior sample, not the highest reward.
            reward = bandits[j].pull()  # Now observe the real reward.
            bandits[j].update(reward)


            rewards[t] = reward  # Save what happened in this trial.
            selected_bandits[t] = j


        self.bandits = bandits  # Make the learned values available for reporting.
        self.rewards = rewards
        self.selected_bandits = selected_bandits

        logger.info("Thompson Sampling experiment completed.")

        return rewards


    def report(self):

        """Log results and save the Thompson Sampling rewards to CSV.

        Reward uses actual observed values, while pseudo-regret measures
        the expected loss from choosing a bandit with a lower true mean.

        Returns:
            dict: Total and average reward, total and average pseudo-regret,
                and the CSV path.

        Raises:
            RuntimeError: If experiment() has not been called.
        """
        if not hasattr(self, "rewards"):
            raise RuntimeError(
                "Run experiment() before report()."
            )

        # Use the same reward and regret measures as Epsilon-Greedy.
        self.cumulative_rewards = np.cumsum(self.rewards)
        total_reward = self.cumulative_rewards[-1]
        average_reward = np.mean(self.rewards)
        optimal_mean = max(b.p for b in self.bandits)

        chosen_means = np.array([
            self.bandits[j].p for j in self.selected_bandits
        ])
        instant_regret = optimal_mean - chosen_means
        self.cumulative_regrets = np.cumsum(instant_regret)
        total_regret = self.cumulative_regrets[-1]
        average_regret = np.mean(instant_regret)


        output_dir = Path(__file__).resolve().parent / "outputs"  # Save everything beside this script.
        output_dir.mkdir(parents=True, exist_ok=True)


        csv_path = output_dir / "thompson_sampling_rewards.csv"  # Separate Thompson results.

        with open(csv_path, "w", newline="") as file:
            writer = csv.writer(file)

            writer.writerow(["Bandit", "Reward", "Algorithm"])

            for j, reward in zip(
                self.selected_bandits, self.rewards
            ):
                writer.writerow([
                    int(j) + 1,
                    float(reward),
                    "ThompsonSampling"
                ])


        logger.info("===== Thompson Sampling Report =====")
        logger.info(f"Total trials: {len(self.rewards)}")
        logger.info(f"Cumulative reward: {total_reward:.2f}")
        logger.info(f"Average reward: {average_reward:.4f}")
        logger.info(f"Cumulative regret: {total_regret:.2f}")
        logger.info(f"Average regret: {average_regret:.4f}")
        logger.info(f"Rewards saved to: {csv_path}")

        for i, bandit in enumerate(self.bandits):
            logger.info(
                f"Bandit {i + 1}: "
                f"True mean = {bandit.p}, "
                f"Posterior mean = "
                f"{bandit.posterior_mean:.4f}, "
                f"Selections = {bandit.N}"
            )

        return {
            "total_reward": total_reward,
            "average_reward": average_reward,
            "cumulative_regret": total_regret,
            "average_regret": average_regret,
            "csv_path": csv_path
        }








def comparison():
    """
Run both algorithms, compare their results, and save all outputs.

A fixed random seed makes it easy to reproduce this experiment.
The function creates two reports, four plots, and one combined CSV
containing a row for each algorithm's trials.

Returns:
    tuple: The Epsilon-Greedy and Thompson Sampling report dictionaries.
"""

    # Use the same random sequence each time we run the full comparison.
    np.random.seed(42)

    # Run Epsilon-Greedy
    eg = EpsilonGreedy(0)
    eg.experiment()
    eg_results = eg.report()

    # Run Thompson Sampling
    ts = ThompsonSampling(0)
    ts.experiment()
    ts_results = ts.report()

    # Compare performance
    logger.info("===== ALGORITHM COMPARISON =====")

    logger.info(
        f"Epsilon-Greedy cumulative reward: "
        f"{eg_results['total_reward']:.2f}"
    )
    logger.info(
        f"Thompson Sampling cumulative reward: "
        f"{ts_results['total_reward']:.2f}"
    )

    logger.info(
        f"Epsilon-Greedy cumulative regret: "
        f"{eg_results['cumulative_regret']:.2f}"
    )
    logger.info(
        f"Thompson Sampling cumulative regret: "
        f"{ts_results['cumulative_regret']:.2f}"
    )

    # Generate plots
    viz = Visualization(eg, ts)
    viz.plot1()
    viz.plot2()

    # Export combined CSV
    output_dir = Path(__file__).resolve().parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    csv_path = output_dir / "bandit_rewards.csv"

    with open(csv_path, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["Bandit", "Reward", "Algorithm"])

        for j, reward in zip(eg.selected_bandits, eg.rewards):
            writer.writerow([
                int(j) + 1,
                float(reward),
                "EpsilonGreedy"
            ])

        for j, reward in zip(ts.selected_bandits, ts.rewards):
            writer.writerow([
                int(j) + 1,
                float(reward),
                "ThompsonSampling"
            ])

    logger.info(f"Combined results saved to: {csv_path}")

    return eg_results, ts_results


if __name__ == "__main__":
    comparison()



####### Bonus Part  ########

"""Even though our code works and compares both algorithms,there are a few things we could do to make it better.

1. Run the experiments more than once
   Right now, we run each algorithm only once. Since the
   rewards are random, the results might be different each
   time. We could run both algorithms 100 times and compare
   their average rewards and regrets. This would help us
   understand which algorithm performs better overall.

2. Separate the bandits from the algorithms
   Currently, both algorithms generate their own rewards.
   We could create a separate class that handles the bandits
   and generates rewards. This way, the algorithms would only
   focus on choosing bandits and learning from the results.
   It would also make the code easier to change later.

3. Try different exploration strategies
   For Epsilon-Greedy, we use epsilon = 1/t, as required.
   However, epsilon becomes very small quite quickly, so
   the algorithm might not explore enough. We could try
   other ways of decreasing epsilon and see how they affect
   the results. We could also try every bandit at least once
   before starting the regular experiment.

4. Make the code easier to adjust
   We could keep values like the number of trials, bandit
   means, and precision together at the beginning of the
   program. This would make it easier to test different
   settings. We could also use separate random generators
   for each algorithm so their results can be reproduced
   independently.

5. Add more tests and improve the graphs
   We could write a few tests to check whether rewards and
   posterior values are updated correctly. Also, instead of
   showing results from just one experiment, we could plot
   the average results from multiple runs to get a clearer
   picture of how the algorithms perform.

Overall, these changes would help us get more reliable
results and make the code easier to understand and improve."""