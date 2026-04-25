
\section{Experiment Setup}

This section describes the experimental setup used in this study, including degradation label construction, Weibull parameter estimation, hyperparameter optimization, and model training procedure. The overall experiment was designed to combine data-driven learning with prior knowledge from reliability engineering, particularly through the use of Weibull-based degradation labels and a knowledge-informed training strategy.

\subsection{Degradation Label Construction Based on the Weibull Distribution}

In this experiment, degradation labels were constructed based on the Weibull distribution, which is widely used in reliability engineering and remaining useful life (RUL) prediction. The Weibull distribution is suitable for degradation modelling because of its flexibility in representing different types of failure behaviour, including early failure, random failure, and wear-out failure.

The reliability function of the Weibull distribution is defined as:

\begin{equation}
R(t) = \exp\left[-\left(\frac{t}{\eta}\right)^{\beta}\right],
\end{equation}

where $R(t)$ represents the reliability of the system at time $t$, $\beta$ is the shape parameter, and $\eta$ is the scale parameter, also known as the characteristic life.

The degradation label can be derived from the reliability function as:

\begin{equation}
D(t) = 1 - R(t),
\end{equation}

where $D(t)$ denotes the degradation level at time $t$. This formulation means that degradation increases as reliability decreases. At the beginning of the system lifetime, the degradation value is close to zero. As the system approaches failure, the degradation value gradually increases toward one.

In practice, estimating both Weibull parameters, namely the shape parameter $\beta$ and the scale parameter $\eta$, requires sufficient failure data and detailed statistical analysis. However, failure data are often limited in real-world predictive maintenance problems. Therefore, in this study, the shape parameter $\beta$ was fixed at 2.0. This choice is consistent with reliability engineering assumptions, where $\beta > 1$ generally indicates a wear-out failure mechanism. Specifically, $\beta = 2.0$ represents a system whose failure rate increases over time, which is suitable for modelling degradation processes.

By fixing $\beta$, the degradation label construction becomes more stable and less dependent on limited data. At the same time, it still preserves a realistic representation of the degradation behaviour of mechanical or industrial systems.

\subsection{Estimation of Characteristic Life Using the Weibayes Method}

After fixing the shape parameter at $\beta = 2.0$, the characteristic life $\eta$ was estimated from the training data using the Weibayes method. Weibayes is a practical estimation approach used when the shape parameter is assumed to be known based on prior knowledge, while the scale parameter is estimated from observed lifetime data.

The Weibayes method is particularly useful in situations where the available data are insufficient to estimate both Weibull parameters reliably. Instead of fitting both $\beta$ and $\eta$ simultaneously, the method reduces the estimation problem by fixing $\beta$ and estimating only $\eta$. This improves the robustness of parameter estimation when the dataset is limited.

In this study, the training dataset consists of run-to-failure samples. This means that the complete lifetime of each unit is available and no censoring is considered. Therefore, the observed lifetimes provide a direct basis for estimating the characteristic life of the system.

For complete run-to-failure data, the Weibayes estimate of $\eta$ can be expressed as:

\begin{equation}
\eta = \left(\frac{1}{n}\sum_{i=1}^{n} t_i^{\beta}\right)^{\frac{1}{\beta}},
\end{equation}

where $n$ is the number of training units, $t_i$ is the observed failure time of the $i$-th unit, and $\beta$ is the fixed shape parameter.

The estimated value of $\eta$ was then used to generate Weibull-based degradation labels for the learning model. As a result, the model does not learn only from raw sensor data, but also from degradation targets that reflect prior knowledge about system failure behaviour.

\subsection{Hyperparameter Search Using Random Search}

To determine an appropriate model configuration, random search was employed instead of grid search. Approximately 1000 random trials were conducted in the first stage to explore the hyperparameter space.

Random search was selected because the number of possible hyperparameter combinations is very large. A full grid search would require evaluating every possible combination of parameters, which would lead to excessive computational cost. In contrast, random search samples configurations randomly from predefined ranges, allowing the experiment to explore the search space more efficiently.

This approach is especially useful when only some hyperparameters have a major impact on model performance. Instead of spending equal computational resources on all possible combinations, random search increases the chance of discovering strong configurations with fewer trials.

The hyperparameters explored in the first-stage search include:

\begin{itemize}
    \item batch size: $32$, $64$, $128$, $256$, $512$;
    \item learning rate: $0.1$, $0.01$, $0.001$, $0.0001$;
    \item lambda: continuous values between $0$ and $3$;
    \item number of hidden layers: from $2$ to $7$;
    \item number of units per layer: $16$, $32$, $64$, $128$, $256$;
    \item dropout probability: $0.1$, $0.2$, $0.25$, $0.4$, $0.5$, $0.6$.
\end{itemize}

This search strategy indicates that the neural network architecture was not fixed at the beginning of the experiment. Instead, the architecture itself, including network depth, width, and dropout regularization, was treated as part of the optimization process. This allows the model structure to be selected based on validation performance rather than manual assumptions.

After the first stage of random search, it was observed that most of the top-performing configurations shared a similar architecture. Based on this observation, the network structure, including the number of layers, number of units, and dropout rate, was fixed. A second-stage random search with 500 iterations was then conducted to fine-tune the remaining training-related hyperparameters:

\begin{itemize}
    \item batch size;
    \item learning rate;
    \item lambda.
\end{itemize}

This two-stage hyperparameter optimization strategy improves both efficiency and performance. The first stage identifies a strong architectural backbone, while the second stage focuses on refining the most sensitive training parameters.

\subsection{Model Training Procedure}

The model was trained using the Adam optimizer. Adam was selected because it combines the advantages of momentum-based optimization and adaptive learning rates. Compared with standard stochastic gradient descent, Adam can provide faster and more stable convergence, especially for deep neural networks.

The model was trained by minimizing a loss function that combines data-driven prediction error with knowledge-informed constraints. In this study, the knowledge component is controlled by the hyperparameter $\lambda$. This parameter determines the contribution of the knowledge-informed term to the overall training objective. A larger value of $\lambda$ increases the influence of prior knowledge, while a smaller value makes the model rely more heavily on data fitting.

To reduce the risk of overfitting, early stopping was applied with a patience of 20 epochs. Specifically, if the validation loss did not improve for 20 consecutive epochs, the training process was terminated. This prevents the model from continuing to learn patterns that are specific to the training data but not generalizable to unseen data.

The validation set played an important role in both model training and hyperparameter selection. During training, validation loss was used to monitor generalization performance and trigger early stopping. During hyperparameter search, each candidate configuration was evaluated based on validation performance rather than training loss alone. This ensures that the selected model achieves a balance between fitting the training data and maintaining strong generalization capability.

\subsection{Summary of the Experimental Pipeline}

The complete experimental pipeline can be summarized as follows:

\begin{enumerate}
    \item Construct degradation labels using the Weibull reliability function.
    \item Fix the Weibull shape parameter at $\beta = 2.0$ based on reliability engineering prior knowledge.
    \item Estimate the characteristic life $\eta$ from run-to-failure training data using the Weibayes method.
    \item Generate degradation labels from the estimated Weibull degradation curve.
    \item Conduct a first-stage random search to identify a suitable neural network architecture.
    \item Fix the best-performing architectural structure.
    \item Conduct a second-stage random search to fine-tune batch size, learning rate, and $\lambda$.
    \item Train the final model using the Adam optimizer.
    \item Apply early stopping with a patience of 20 epochs based on validation loss.
    \item Select the final model according to validation performance.
\end{enumerate}

Overall, the experiment combines reliability-based label construction, statistically grounded parameter estimation, efficient hyperparameter optimization, and regularized neural network training. This setup allows the model to learn from both observed data and prior knowledge about degradation behaviour, which is consistent with the informed machine learning framework discussed in this report.