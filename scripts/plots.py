import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties
from typing import List, Dict, Optional, Tuple, Any
from scipy.spatial import ConvexHull


def plot_optimization_results(
    data_series: List[Dict],
    title: str,
    xlabel: str = "Number of Rollouts",
    ylabel: str = "Score",
    figsize: Tuple[int, int] = (11, 7),
    color_map: Optional[Dict[str, str]] = None,
    opt_nicknames: Optional[Dict[str, str]] = None,
    legend_title: str = "Optimization Method",
    output_filename: Optional[str] = None,
    cumulative_max: bool = True,
    show_grid: bool = True,
    show_plot: bool = True,
):
    """
    Generic plotting function for optimization results with customizable styling.

    Parameters:
    -----------
    data_series : List[Dict]
        List of dictionaries, each containing:
        - 'x': x-axis data (e.g., eval counts)
        - 'y': y-axis data (e.g., scores)
        - 'label': label for the series
        - 'color': (optional) color for the line, defaults to black
        - 'marker': (optional) marker style, defaults to 'o'
        - 'linewidth': (optional) line width, defaults to 3
        - 'markersize': (optional) marker size, defaults to 6
    title : str
        Plot title
    xlabel : str
        X-axis label
    ylabel : str
        Y-axis label
    figsize : Tuple[int, int]
        Figure size (width, height)
    color_map : Optional[Dict[str, str]]
        Dictionary mapping optimizer names to colors
    opt_nicknames : Optional[Dict[str, str]]
        Dictionary mapping full names to display names
    legend_title : str
        Title for the legend
    output_filename : Optional[str]
        If provided, saves the plot to this filename
    cumulative_max : bool
        If True, applies np.maximum.accumulate to y-values
    show_grid : bool
        If True, displays grid
    show_plot : bool
        If True, calls plt.show()

    Returns:
    --------
    fig, ax : matplotlib figure and axes objects

    Example:
    --------
    data_series = [
        {
            'x': [1, 2, 3, 4, 5],
            'y': [10, 15, 12, 18, 20],
            'label': 'Method A',
            'color': 'blue'
        },
        {
            'x': [1, 2, 3, 4, 5],
            'y': [8, 14, 16, 17, 19],
            'label': 'Method B',
            'color': 'red'
        }
    ]

    fig, ax = plot_optimization_results(
        data_series=data_series,
        title="My Optimization Results",
        output_filename="results.png"
    )
    """

    # Default color map
    if color_map is None:
        color_map = {
            "grey": "#888888",
            "green": "#44b36d",
            "orange": "#f5a142",
            "light_blue": "#bbdefb",
            "medium_blue": "#64b5f6",
            "deep_blue": "#1976d2",
            "darkest_blue": "#0d47a1",
        }

    if opt_nicknames is None:
        opt_nicknames = {}

    # Font configurations
    XTICK_FONT = {"fontsize": 21, "fontweight": "bold"}
    YTICK_FONT = {"fontsize": 21, "fontweight": "bold"}
    TITLE_FONT = {"fontsize": 26, "fontweight": "bold"}
    XLABEL_FONT = {"fontsize": 22, "fontweight": "bold"}
    YLABEL_FONT = {"fontsize": 22, "fontweight": "bold"}
    LEGEND_FONT = FontProperties(family="sans-serif", size=17, weight="bold")

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    # Plot each series
    for series in data_series:
        x = series["x"]
        y = series["y"]

        # Apply cumulative maximum if requested
        if cumulative_max:
            y = np.maximum.accumulate(y)

        # Get optional parameters with defaults
        color = series.get("color", "black")
        marker = series.get("marker", "o")
        linewidth = series.get("linewidth", 3)
        markersize = series.get("markersize", 6)
        label = series.get("label", "")

        ax.plot(
            x,
            y,
            label=label,
            marker=marker,
            color=color,
            linewidth=linewidth,
            markersize=markersize,
        )

    # Set title and labels
    ax.set_title(title, fontdict=TITLE_FONT)
    ax.set_xlabel(xlabel, fontdict=XLABEL_FONT)
    ax.set_ylabel(ylabel, fontdict=YLABEL_FONT)

    # Set tick label fonts
    ax.tick_params(axis="x", labelsize=XTICK_FONT["fontsize"], width=1)
    ax.tick_params(axis="y", labelsize=YTICK_FONT["fontsize"], width=1)

    for label in ax.get_xticklabels():
        label.set_fontweight(XTICK_FONT["fontweight"])
    for label in ax.get_yticklabels():
        label.set_fontweight(YTICK_FONT["fontweight"])

    # Create legend with sorted handles
    handles, labels = ax.get_legend_handles_labels()

    def get_opt_from_label(label):
        """Extracts the opt part from label (first word before space and paren)"""
        return label.split()[0]

    # Create order based on color_map keys
    order = {opt: i for i, opt in enumerate(color_map.keys())}

    # Sort handles and labels
    sorted_items = sorted(
        zip(handles, labels),
        key=lambda x: order.get(get_opt_from_label(x[1]), float("inf")),
    )

    # Create line-only handles (no markers)
    sorted_handles = [
        plt.Line2D(
            [],
            [],
            color=handle.get_color(),
            linewidth=handle.get_linewidth(),
            linestyle="-",
        )
        for handle, _ in sorted_items
    ]

    # Apply nicknames and clean up labels
    sorted_labels = [
        opt_nicknames.get(label, label).replace(" (24000 rollouts)", "")
        for _, label in sorted_items
    ]

    # Add legend
    ax.legend(
        sorted_handles,
        sorted_labels,
        title=legend_title,
        prop=LEGEND_FONT,
        title_fontproperties=LEGEND_FONT,
        framealpha=1.0,
    )

    # Add grid if requested
    if show_grid:
        plt.grid()

    plt.tight_layout()

    # Save if filename provided
    if output_filename:
        plt.savefig(output_filename, dpi=300, bbox_inches="tight")

    # Show plot if requested
    if show_plot:
        plt.show()

    return fig, ax


def plot_two_stage_optimization(
    warmup_model,
    dynamic_model,
    label: str = "AdaGEPA",
    color: str = "blue",
    title: str = "Optimization Results",
    xlabel: str = "Number of Rollouts",
    ylabel: str = "Score",
    figsize: Tuple[int, int] = (11, 7),
    output_filename: Optional[str] = None,
    cumulative_max: bool = True,
    show_grid: bool = True,
    show_plot: bool = True,
    combine_stages: bool = True,
    warmup_label: Optional[str] = None,
    dynamic_label: Optional[str] = None,
    warmup_color: Optional[str] = None,
    dynamic_color: Optional[str] = None,
    show_transition_line: bool = True,
    transition_line_color: str = "gray",
    transition_line_style: str = "--",
    transition_line_width: float = 2.0,
):
    """
    Plot learning curves for two-stage optimization (warmup + dynamic stages).
    
    This function handles the fact that GEPA resets max_metric_calls between stages,
    properly offsetting the dynamic stage's eval counts by the warmup stage's total
    metric calls to create a continuous learning curve.
    
    Parameters:
    -----------
    warmup_model : dspy model
        The model from the warmup stage with detailed_results attribute
    dynamic_model : dspy model
        The model from the dynamic stage with detailed_results attribute
    label : str
        Label for the combined curve (used when combine_stages=True)
    color : str
        Color for the combined curve (used when combine_stages=True)
    title : str
        Plot title
    xlabel : str
        X-axis label
    ylabel : str
        Y-axis label
    figsize : Tuple[int, int]
        Figure size (width, height)
    output_filename : Optional[str]
        If provided, saves the plot to this filename
    cumulative_max : bool
        If True, applies np.maximum.accumulate to y-values
    show_grid : bool
        If True, displays grid
    show_plot : bool
        If True, calls plt.show()
    combine_stages : bool
        If True, plots as a single combined curve. If False, plots warmup and dynamic
        as separate series.
    warmup_label : Optional[str]
        Label for warmup stage (used when combine_stages=False)
    dynamic_label : Optional[str]
        Label for dynamic stage (used when combine_stages=False)
    warmup_color : Optional[str]
        Color for warmup stage (used when combine_stages=False)
    dynamic_color : Optional[str]
        Color for dynamic stage (used when combine_stages=False)
    show_transition_line : bool
        If True, displays a vertical dotted line at the transition between warmup and dynamic stages
    transition_line_color : str
        Color for the transition line (default: "gray")
    transition_line_style : str
        Line style for the transition line (default: "--" for dotted)
    transition_line_width : float
        Line width for the transition line (default: 2.0)
    
    Returns:
    --------
    fig, ax : matplotlib figure and axes objects
    
    Example:
    --------
    warmup_model = dspy.load("trained_models/dbbio/mistral_small/warmup", allow_pickle=True)
    dynamic_model = dspy.load("trained_models/dbbio/mistral_small/dynamic", allow_pickle=True)
    
    fig, ax = plot_two_stage_optimization(
        warmup_model=warmup_model,
        dynamic_model=dynamic_model,
        label="AdaGEPA",
        color="blue",
        title="DBBio, Mistral-small",
        output_filename="dbbio_learning_curve.png"
    )
    """
    
    # Extract data from warmup stage
    warmup_eval_counts = warmup_model.detailed_results.discovery_eval_counts
    warmup_scores = warmup_model.detailed_results.val_aggregate_scores
    warmup_total_calls = warmup_model.detailed_results.total_metric_calls
    
    # Extract data from dynamic stage
    dynamic_eval_counts = dynamic_model.detailed_results.discovery_eval_counts
    dynamic_scores = dynamic_model.detailed_results.val_aggregate_scores
    
    # Offset dynamic stage's eval counts by warmup's total metric calls
    # This accounts for the fact that GEPA resets max_metric_calls between stages
    dynamic_eval_counts_offset = [
        count + warmup_total_calls for count in dynamic_eval_counts
    ]
    
    # Font configurations
    XTICK_FONT = {"fontsize": 21, "fontweight": "bold"}
    YTICK_FONT = {"fontsize": 21, "fontweight": "bold"}
    TITLE_FONT = {"fontsize": 26, "fontweight": "bold"}
    XLABEL_FONT = {"fontsize": 22, "fontweight": "bold"}
    YLABEL_FONT = {"fontsize": 22, "fontweight": "bold"}
    LEGEND_FONT = FontProperties(family="sans-serif", size=17, weight="bold")
    
    # Create figure
    fig, ax = plt.subplots(figsize=figsize)
    
    if combine_stages:
        # Combine stages into a single continuous curve
        combined_eval_counts = list(warmup_eval_counts) + dynamic_eval_counts_offset
        combined_scores = list(warmup_scores) + list(dynamic_scores)
        
        # Apply cumulative maximum if requested
        if cumulative_max:
            combined_scores = np.maximum.accumulate(combined_scores)
        
        ax.plot(
            combined_eval_counts,
            combined_scores,
            label=label,
            marker="o",
            color=color,
            linewidth=3,
            markersize=6,
        )
    else:
        # Plot stages separately
        warmup_label = warmup_label or "Warmup"
        dynamic_label = dynamic_label or "Dynamic"
        warmup_color = warmup_color or "black"
        dynamic_color = dynamic_color or "blue"
        
        # Apply cumulative maximum if requested
        warmup_scores_plot = warmup_scores
        dynamic_scores_plot = dynamic_scores
        if cumulative_max:
            warmup_scores_plot = np.maximum.accumulate(warmup_scores)
            # For dynamic stage, we need to consider the warmup's final score
            if len(warmup_scores) > 0:
                dynamic_scores_with_warmup = [warmup_scores[-1]] + list(dynamic_scores)
                dynamic_scores_plot = np.maximum.accumulate(dynamic_scores_with_warmup)[1:]
            else:
                dynamic_scores_plot = np.maximum.accumulate(dynamic_scores)
        
        ax.plot(
            warmup_eval_counts,
            warmup_scores_plot,
            label=warmup_label,
            marker="o",
            color=warmup_color,
            linewidth=3,
            markersize=6,
        )
        
        ax.plot(
            dynamic_eval_counts_offset,
            dynamic_scores_plot,
            label=dynamic_label,
            marker="o",
            color=dynamic_color,
            linewidth=3,
            markersize=6,
        )
    
    # Add vertical line to show transition between warmup and dynamic stages
    if show_transition_line:
        ax.axvline(
            x=warmup_total_calls,
            ymin=0,
            ymax=1,
            color=transition_line_color,
            linestyle=transition_line_style,
            linewidth=transition_line_width,
            alpha=0.7,
            zorder=0,  # Draw behind the data lines
        )
    
    # Set title and labels
    ax.set_title(title, fontdict=TITLE_FONT)
    ax.set_xlabel(xlabel, fontdict=XLABEL_FONT)
    ax.set_ylabel(ylabel, fontdict=YLABEL_FONT)
    
    # Set tick label fonts
    ax.tick_params(axis="x", labelsize=XTICK_FONT["fontsize"], width=1)
    ax.tick_params(axis="y", labelsize=YTICK_FONT["fontsize"], width=1)
    
    for label in ax.get_xticklabels():
        label.set_fontweight(XTICK_FONT["fontweight"])
    for label in ax.get_yticklabels():
        label.set_fontweight(YTICK_FONT["fontweight"])
    
    # Add legend
    ax.legend(
        prop=LEGEND_FONT,
        title_fontproperties=LEGEND_FONT,
        framealpha=1.0,
    )
    
    # Add grid if requested
    if show_grid:
        plt.grid()
    
    plt.tight_layout()
    
    # Save if filename provided
    if output_filename:
        plt.savefig(output_filename, dpi=300, bbox_inches="tight")
    
    # Show plot if requested
    if show_plot:
        plt.show()
    
    return fig, ax


def plot_two_stage_optimization_and_mipro(
    warmup_model,
    dynamic_model,
    mipro_model,
    label: str = "AdaGEPA",
    color: str = "blue",
    mipro_label: str = "MIPROv2",
    mipro_color: str = "yellow",
    simple_feedback_model: Optional[Any] = None,
    simple_feedback_label: str = "GEPA Simple Feedback",
    simple_feedback_color: str = "orange",
    rich_feedback_model: Optional[Any] = None,
    rich_feedback_label: str = "GEPA Rich Feedback",
    rich_feedback_color: str = "red",
    title: str = "Optimization Results",
    xlabel: str = "Number of Rollouts",
    ylabel: str = "Score",
    figsize: Tuple[int, int] = (11, 7),
    output_filename: Optional[str] = None,
    cumulative_max: bool = True,
    show_grid: bool = True,
    show_plot: bool = True,
    combine_stages: bool = True,
    warmup_label: Optional[str] = None,
    dynamic_label: Optional[str] = None,
    warmup_color: Optional[str] = None,
    dynamic_color: Optional[str] = None,
    show_transition_line: bool = True,
    transition_line_color: str = "gray",
    transition_line_style: str = "--",
    transition_line_width: float = 2.0,
    validation_set_size: int = 111,
):
    """
    Plot learning curves for two-stage optimization (warmup + dynamic stages), MIPROv2,
    and optionally GEPA simple/rich feedback models.
    
    This function extends plot_two_stage_optimization to also include a MIPROv2 curve
    and optionally GEPA simple/rich feedback models. It handles the fact that GEPA resets
    max_metric_calls between stages, properly offsetting the dynamic stage's eval counts
    by the warmup stage's total metric calls to create a continuous learning curve.
    
    Parameters:
    -----------
    warmup_model : dspy model
        The model from the warmup stage with detailed_results attribute
    dynamic_model : dspy model
        The model from the dynamic stage with detailed_results attribute
    mipro_model : dspy model
        The MIPROv2 model with trial_logs attribute
    label : str
        Label for the combined curve (used when combine_stages=True)
    color : str
        Color for the combined curve (used when combine_stages=True)
    mipro_label : str
        Label for the MIPROv2 curve
    mipro_color : str
        Color for the MIPROv2 curve (default: "yellow")
    simple_feedback_model : Optional[dspy model]
        Optional GEPA model with simple feedback only (has detailed_results attribute)
    simple_feedback_label : str
        Label for the simple feedback curve (default: "GEPA Simple Feedback")
    simple_feedback_color : str
        Color for the simple feedback curve (default: "orange")
    rich_feedback_model : Optional[dspy model]
        Optional GEPA model with rich feedback only (has detailed_results attribute)
    rich_feedback_label : str
        Label for the rich feedback curve (default: "GEPA Rich Feedback")
    rich_feedback_color : str
        Color for the rich feedback curve (default: "red")
    title : str
        Plot title
    xlabel : str
        X-axis label
    ylabel : str
        Y-axis label
    figsize : Tuple[int, int]
        Figure size (width, height)
    output_filename : Optional[str]
        If provided, saves the plot to this filename
    cumulative_max : bool
        If True, applies np.maximum.accumulate to y-values
    show_grid : bool
        If True, displays grid
    show_plot : bool
        If True, calls plt.show()
    combine_stages : bool
        If True, plots as a single combined curve. If False, plots warmup and dynamic
        as separate series.
    warmup_label : Optional[str]
        Label for warmup stage (used when combine_stages=False)
    dynamic_label : Optional[str]
        Label for dynamic stage (used when combine_stages=False)
    warmup_color : Optional[str]
        Color for warmup stage (used when combine_stages=False)
    dynamic_color : Optional[str]
        Color for dynamic stage (used when combine_stages=False)
    show_transition_line : bool
        If True, displays a vertical dotted line at the transition between warmup and dynamic stages
    transition_line_color : str
        Color for the transition line (default: "gray")
    transition_line_style : str
        Line style for the transition line (default: "--" for dotted)
    transition_line_width : float
        Line width for the transition line (default: 2.0)
    validation_set_size : int
        Size of the validation set used to normalize MIPROv2 scores (default: 111)
    
    Returns:
    --------
    fig, ax : matplotlib figure and axes objects
    
    Example:
    --------
    warmup_model = dspy.load("trained_models/dbbio/mistral_small/warmup", allow_pickle=True)
    dynamic_model = dspy.load("trained_models/dbbio/mistral_small/dynamic", allow_pickle=True)
    mipro_model = dspy.load("./mipro_exp/miprov2_medqa_mistral_small", allow_pickle=True)
    simple_model = dspy.load("./mipro_exp/gepa_simple_feedback_medqa_mistral_small", allow_pickle=True)
    rich_model = dspy.load("./mipro_exp/gepa_rich_feedback_medqa_mistral_small", allow_pickle=True)
    
    fig, ax = plot_two_stage_optimization_and_mipro(
        warmup_model=warmup_model,
        dynamic_model=dynamic_model,
        mipro_model=mipro_model,
        simple_feedback_model=simple_model,
        rich_feedback_model=rich_model,
        label="AdaGEPA",
        color="blue",
        mipro_label="MIPROv2",
        mipro_color="yellow",
        title="DBBio, Mistral-small",
        output_filename="dbbio_learning_curve.png"
    )
    """
    
    # Extract data from warmup stage
    warmup_eval_counts = warmup_model.detailed_results.discovery_eval_counts
    warmup_scores = warmup_model.detailed_results.val_aggregate_scores
    warmup_total_calls = warmup_model.detailed_results.total_metric_calls
    
    # Extract data from dynamic stage
    dynamic_eval_counts = dynamic_model.detailed_results.discovery_eval_counts
    dynamic_scores = dynamic_model.detailed_results.val_aggregate_scores
    
    # Offset dynamic stage's eval counts by warmup's total metric calls
    # This accounts for the fact that GEPA resets max_metric_calls between stages
    dynamic_eval_counts_offset = [
        count + warmup_total_calls for count in dynamic_eval_counts
    ]
    
    # Calculate max GEPA rollouts to cap MIPROv2 data
    all_gepa_eval_counts = list(warmup_eval_counts) + dynamic_eval_counts_offset
    max_gepa_rollouts = max(all_gepa_eval_counts) if len(all_gepa_eval_counts) > 0 else None
    
    # Extract data from MIPROv2 trial_logs
    trial_logs = mipro_model.trial_logs
    mipro_eval_counts = []
    mipro_scores = []
    
    # Sort by trial number (key) to ensure correct order
    sorted_trials = sorted(trial_logs.items(), key=lambda x: x[0])
    
    for trial_num, trial_data in sorted_trials:
        # Extract eval count
        if 'total_eval_calls_so_far' in trial_data:
            eval_count = trial_data['total_eval_calls_so_far']
            
            # Cap eval count at max GEPA rollouts if specified
            if max_gepa_rollouts is not None and eval_count > max_gepa_rollouts:
                continue  # Skip this data point if it exceeds GEPA max
            
            # Extract score (prefer full_eval_score, fallback to mb_score)
            score = None
            if 'full_eval_score' in trial_data:
                score = trial_data['full_eval_score']
            elif 'mb_score' in trial_data:
                score = trial_data['mb_score']
            
            # Only add if we have both eval_count and score
            if score is not None:
                # Normalize score by validation set size
                normalized_score = score / validation_set_size
                mipro_eval_counts.append(eval_count)
                mipro_scores.append(normalized_score)
    
    # Extract data from simple feedback model (if provided)
    simple_feedback_eval_counts = []
    simple_feedback_scores = []
    if simple_feedback_model is not None:
        simple_feedback_eval_counts = simple_feedback_model.detailed_results.discovery_eval_counts
        simple_feedback_scores = simple_feedback_model.detailed_results.val_aggregate_scores
    
    # Extract data from rich feedback model (if provided)
    rich_feedback_eval_counts = []
    rich_feedback_scores = []
    if rich_feedback_model is not None:
        rich_feedback_eval_counts = rich_feedback_model.detailed_results.discovery_eval_counts
        rich_feedback_scores = rich_feedback_model.detailed_results.val_aggregate_scores
    
    # Font configurations
    XTICK_FONT = {"fontsize": 21, "fontweight": "bold"}
    YTICK_FONT = {"fontsize": 21, "fontweight": "bold"}
    TITLE_FONT = {"fontsize": 26, "fontweight": "bold"}
    XLABEL_FONT = {"fontsize": 22, "fontweight": "bold"}
    YLABEL_FONT = {"fontsize": 22, "fontweight": "bold"}
    LEGEND_FONT = FontProperties(family="sans-serif", size=17, weight="bold")
    
    # Create figure
    fig, ax = plt.subplots(figsize=figsize)
    
    if combine_stages:
        # Combine stages into a single continuous curve
        combined_eval_counts = list(warmup_eval_counts) + dynamic_eval_counts_offset
        combined_scores = list(warmup_scores) + list(dynamic_scores)
        
        # Apply cumulative maximum if requested
        if cumulative_max:
            combined_scores = np.maximum.accumulate(combined_scores)
        
        ax.plot(
            combined_eval_counts,
            combined_scores,
            label=label,
            marker="o",
            color=color,
            linewidth=3,
            markersize=6,
        )
    else:
        # Plot stages separately
        warmup_label = warmup_label or "Warmup"
        dynamic_label = dynamic_label or "Dynamic"
        warmup_color = warmup_color or "black"
        dynamic_color = dynamic_color or "blue"
        
        # Apply cumulative maximum if requested
        warmup_scores_plot = warmup_scores
        dynamic_scores_plot = dynamic_scores
        if cumulative_max:
            warmup_scores_plot = np.maximum.accumulate(warmup_scores)
            # For dynamic stage, we need to consider the warmup's final score
            if len(warmup_scores) > 0:
                dynamic_scores_with_warmup = [warmup_scores[-1]] + list(dynamic_scores)
                dynamic_scores_plot = np.maximum.accumulate(dynamic_scores_with_warmup)[1:]
            else:
                dynamic_scores_plot = np.maximum.accumulate(dynamic_scores)
        
        ax.plot(
            warmup_eval_counts,
            warmup_scores_plot,
            label=warmup_label,
            marker="o",
            color=warmup_color,
            linewidth=3,
            markersize=6,
        )
        
        ax.plot(
            dynamic_eval_counts_offset,
            dynamic_scores_plot,
            label=dynamic_label,
            marker="o",
            color=dynamic_color,
            linewidth=3,
            markersize=6,
        )
    
    # Plot MIPROv2 curve
    if len(mipro_eval_counts) > 0 and len(mipro_scores) > 0:
        mipro_scores_plot = mipro_scores
        if cumulative_max:
            mipro_scores_plot = np.maximum.accumulate(mipro_scores)
        
        ax.plot(
            mipro_eval_counts,
            mipro_scores_plot,
            label=mipro_label,
            marker="o",
            color=mipro_color,
            linewidth=3,
            markersize=6,
        )
    
    # Plot simple feedback model curve (if provided)
    if len(simple_feedback_eval_counts) > 0 and len(simple_feedback_scores) > 0:
        simple_feedback_scores_plot = simple_feedback_scores
        if cumulative_max:
            simple_feedback_scores_plot = np.maximum.accumulate(simple_feedback_scores)
        
        ax.plot(
            simple_feedback_eval_counts,
            simple_feedback_scores_plot,
            label=simple_feedback_label,
            marker="o",
            color=simple_feedback_color,
            linewidth=3,
            markersize=6,
        )
    
    # Plot rich feedback model curve (if provided)
    if len(rich_feedback_eval_counts) > 0 and len(rich_feedback_scores) > 0:
        rich_feedback_scores_plot = rich_feedback_scores
        if cumulative_max:
            rich_feedback_scores_plot = np.maximum.accumulate(rich_feedback_scores)
        
        ax.plot(
            rich_feedback_eval_counts,
            rich_feedback_scores_plot,
            label=rich_feedback_label,
            marker="o",
            color=rich_feedback_color,
            linewidth=3,
            markersize=6,
        )
    
    # Add vertical line to show transition between warmup and dynamic stages
    if show_transition_line:
        ax.axvline(
            x=warmup_total_calls,
            ymin=0,
            ymax=1,
            color=transition_line_color,
            linestyle=transition_line_style,
            linewidth=transition_line_width,
            alpha=0.7,
            zorder=0,  # Draw behind the data lines
        )
    
    # Set title and labels
    ax.set_title(title, fontdict=TITLE_FONT)
    ax.set_xlabel(xlabel, fontdict=XLABEL_FONT)
    ax.set_ylabel(ylabel, fontdict=YLABEL_FONT)
    
    # Set tick label fonts
    ax.tick_params(axis="x", labelsize=XTICK_FONT["fontsize"], width=1)
    ax.tick_params(axis="y", labelsize=YTICK_FONT["fontsize"], width=1)
    
    for label in ax.get_xticklabels():
        label.set_fontweight(XTICK_FONT["fontweight"])
    for label in ax.get_yticklabels():
        label.set_fontweight(YTICK_FONT["fontweight"])
    
    # Add legend
    ax.legend(
        prop=LEGEND_FONT,
        title_fontproperties=LEGEND_FONT,
        framealpha=1.0,
    )
    
    # Add grid if requested
    if show_grid:
        plt.grid()
    
    plt.tight_layout()
    
    # Save if filename provided
    if output_filename:
        plt.savefig(output_filename, dpi=300, bbox_inches="tight")
    
    # Show plot if requested
    if show_plot:
        plt.show()
    
    return fig, ax


def compute_pareto_frontier(privacy_scores, utility_scores):
    """
    Compute the Pareto frontier from privacy and utility scores.
    
    A solution is on the Pareto frontier if there's no other solution that has
    both higher privacy AND higher utility.
    
    Parameters:
    -----------
    privacy_scores : array-like
        Privacy scores (higher is better)
    utility_scores : array-like
        Utility scores (higher is better)
    
    Returns:
    --------
    pareto_indices : list
        Indices of solutions on the Pareto frontier
    """
    pareto_indices = []
    n = len(privacy_scores)
    
    for i in range(n):
        is_dominated = False
        for j in range(n):
            if i != j:
                # Check if solution j dominates solution i
                # j dominates i if j has both higher privacy AND higher utility
                if (privacy_scores[j] >= privacy_scores[i] and 
                    utility_scores[j] >= utility_scores[i] and
                    (privacy_scores[j] > privacy_scores[i] or 
                     utility_scores[j] > utility_scores[i])):
                    is_dominated = True
                    break
        
        if not is_dominated:
            pareto_indices.append(i)
    
    # Sort Pareto frontier points by privacy score (ascending) for plotting
    pareto_indices.sort(key=lambda idx: privacy_scores[idx])
    
    return pareto_indices


def plot_pareto_frontier(
    model,
    task,
    test_set_size: int = 10,
    candidate_set_size: int = 10,
    models_dict: Optional[Dict[str, any]] = None,
    model_labels: Optional[Dict[str, str]] = None,
    figsize: Tuple[int, int] = (10, 8),
    title: Optional[str] = None,
    output_filename: Optional[str] = None,
    show_plot: bool = True,
    show_grid: bool = True,
    alpha: float = 0.5,
    frontier_color: str = "black",
    frontier_linewidth: float = 2.5,
):
    """
    Plot Pareto frontier visualization for optimization candidates.
    
    Creates a 2D scatter plot showing all candidate prompts discovered during
    optimization, with privacy on X-axis and utility on Y-axis. Supports
    multiple models per task, each with different colors and shapes.
    
    Parameters:
    -----------
    model : dspy model or None
        Single optimized model with detailed_results.candidates attribute.
        If models_dict is provided, this is ignored.
    task : Task object
        Task object with compute_privacy and compute_utility methods
    test_set_size : int
        Number of test examples to use for evaluation (default: 10)
    candidate_set_size : int
        Maximum number of candidates to evaluate per model (default: 10)
    models_dict : Optional[Dict[str, any]]
        Dictionary mapping model names to dspy models. If provided, multiple
        models will be plotted with different colors and shapes.
    model_labels : Optional[Dict[str, str]]
        Optional dictionary mapping model names to display labels
    figsize : Tuple[int, int]
        Figure size (width, height)
    title : Optional[str]
        Plot title. If None, uses "Pareto Frontier Visualization"
    output_filename : Optional[str]
        If provided, saves the plot to this filename
    show_plot : bool
        If True, calls plt.show()
    show_grid : bool
        If True, displays grid
    alpha : float
        Transparency of scatter points (default: 0.5)
    frontier_color : str
        Color for Pareto frontier line (default: "black")
    frontier_linewidth : float
        Line width for Pareto frontier (default: 2.5)
    
    Returns:
    --------
    fig, ax : matplotlib figure and axes objects
    """
    import dspy
    import numpy as np
    
    # Default colors and markers for different models
    default_colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", 
                     "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]
    default_markers = ["o", "s", "v", "^", "D", "p", "*", "h", "X", "P"]
    
    # Determine if we have multiple models
    if models_dict is not None:
        model_names = list(models_dict.keys())
        models_to_plot = models_dict
    else:
        # Single model case - convert to dict format
        model_names = ["Model"]
        models_to_plot = {"Model": model}
    
    n_models = len(model_names)
    
    # Create evaluator with test set
    evaluator = dspy.Evaluate(
        devset=task.examples_test[:test_set_size],
        num_threads=8,
        display_progress=False,
        provide_traceback=False,
    )
    
    # Collect all scores from all models
    all_scores = []
    model_info = []  # Track which model each score belongs to
    
    for model_idx, model_name in enumerate(model_names):
        model_obj = models_to_plot[model_name]
        
        # Extract candidates
        candidates = model_obj.detailed_results.candidates[:candidate_set_size]
        n_candidates = len(candidates)
        
        if n_candidates == 0:
            print(f"Warning: No candidates found for {model_name}")
            continue
        
        # Evaluate all candidates
        print(f"[{model_name}] Evaluating {n_candidates} candidates on {test_set_size} test examples...")
        for i, candidate in enumerate(candidates):
            privacy_result = evaluator(candidate, metric=task.compute_privacy)
            utility_result = evaluator(candidate, metric=task.compute_utility)
            print(f"Privacy score: {privacy_result.score}, Utility score: {utility_result.score}")
            all_scores.append({
                "privacy": privacy_result.score,
                "utility": utility_result.score,
            })
            model_info.append(model_idx)
            if (i + 1) % 10 == 0:
                print(f"  Evaluated {i + 1}/{n_candidates} candidates...")
    
    if len(all_scores) == 0:
        raise ValueError("No candidates found in any model")
    
    # Convert to arrays
    privacy_scores = np.array([s["privacy"] for s in all_scores])
    utility_scores = np.array([s["utility"] for s in all_scores])
    model_indices = np.array(model_info)
    
    # Compute Pareto frontier across all models
    pareto_indices = compute_pareto_frontier(privacy_scores, utility_scores)
    n_pareto = len(pareto_indices)
    
    print(f"Found {n_pareto} non-dominated solutions on the Pareto frontier")
    
    # Font configurations
    XTICK_FONT = {"fontsize": 18, "fontweight": "bold"}
    YTICK_FONT = {"fontsize": 18, "fontweight": "bold"}
    TITLE_FONT = {"fontsize": 24, "fontweight": "bold"}
    XLABEL_FONT = {"fontsize": 20, "fontweight": "bold"}
    YLABEL_FONT = {"fontsize": 20, "fontweight": "bold"}
    
    # Create figure
    fig, ax = plt.subplots(figsize=figsize)
    
    # Store handles for legend
    legend_handles = []
    
    # Plot candidates for each model with different colors and shapes
    for model_idx, model_name in enumerate(model_names):
        # Get color and marker for this model
        color = default_colors[model_idx % len(default_colors)]
        marker = default_markers[model_idx % len(default_markers)]
        
        # Get label
        if model_labels and model_name in model_labels:
            label = model_labels[model_name]
        else:
            label = model_name
        
        # Filter scores for this model
        model_mask = model_indices == model_idx
        model_privacy = privacy_scores[model_mask]
        model_utility = utility_scores[model_mask]
        
        if len(model_privacy) > 0:
            # Plot convex hull (exploration region) if we have at least 3 points
            if len(model_privacy) >= 3:
                try:
                    points = np.column_stack((model_privacy, model_utility))
                    hull = ConvexHull(points)
                    # Plot filled region
                    for simplex in hull.simplices:
                        ax.fill(
                            points[simplex, 0],
                            points[simplex, 1],
                            color=color,
                            alpha=0.15,
                            edgecolor=None,
                            zorder=1,
                        )
                    # Plot hull outline
                    hull_points = points[hull.vertices]
                    print(f"Hull points privacy: {np.append(hull_points[:, 0], hull_points[0, 0])}, Hull points utility: {np.append(hull_points[:, 1], hull_points[0, 1])}")
                    ax.plot(
                        np.append(hull_points[:, 0], hull_points[0, 0]),
                        np.append(hull_points[:, 1], hull_points[0, 1]),
                        color=color,
                        linewidth=1.5,
                        alpha=0.4,
                        linestyle="-",
                        zorder=2,
                    )
                except:
                    # If convex hull fails (e.g., collinear points), skip region
                    pass
            
            # Plot scatter points
            scatter = ax.scatter(
                model_privacy,
                model_utility,
                c=color,
                marker=marker,
                alpha=alpha,
                s=50,
                edgecolors="black",
                linewidths=0.5,
                label=label,
                zorder=3,
            )
            legend_handles.append(scatter)
    
    # Plot Pareto frontier line (but don't highlight dots differently)
    if n_pareto > 0:
        pareto_privacy = privacy_scores[pareto_indices]
        pareto_utility = utility_scores[pareto_indices]
        
        # Draw connected line for Pareto frontier
        print(f"Pareto privacy: {pareto_privacy}, Pareto utility: {pareto_utility}")
        ax.plot(
            pareto_privacy,
            pareto_utility,
            color=frontier_color,
            linewidth=frontier_linewidth,
            linestyle="--",
            alpha=0.8,
            zorder=4,  # Draw above scatter points but below any highlights
        )
    
    # Set title and labels
    if title is None:
        title = ""
    ax.set_title(title, fontdict=TITLE_FONT)
    ax.set_xlabel("Privacy Score (%)", fontdict=XLABEL_FONT)
    ax.set_ylabel("Utility Score (%)", fontdict=YLABEL_FONT)
    
    # Set tick label fonts
    ax.tick_params(axis="x", labelsize=XTICK_FONT["fontsize"], width=1)
    ax.tick_params(axis="y", labelsize=YTICK_FONT["fontsize"], width=1)
    
    for label in ax.get_xticklabels():
        label.set_fontweight(XTICK_FONT["fontweight"])
    for label in ax.get_yticklabels():
        label.set_fontweight(YTICK_FONT["fontweight"])
    
    # Add legend
    if len(legend_handles) > 0:
        LEGEND_FONT = FontProperties(family="sans-serif", size=14, weight="bold")
        ax.legend(
            handles=legend_handles,
            prop=LEGEND_FONT,
            title_fontproperties=LEGEND_FONT,
            framealpha=1.0,
            loc="best",
        )
    
    # Add grid if requested
    if show_grid:
        plt.grid(alpha=0.3)
    
    plt.tight_layout()
    
    # Save if filename provided
    if output_filename:
        plt.savefig(output_filename, dpi=300, bbox_inches="tight")
        print(f"Plot saved to {output_filename}")
    
    # Show plot if requested
    if show_plot:
        plt.show()
    
    return fig, ax


def plot_pareto_frontier_multi_task(
    models_dict: Dict[str, any],
    tasks_dict: Dict[str, any],
    test_set_size: int = 10,
    candidate_set_size: int = 10,
    models_per_task: Optional[Dict[str, Dict[str, any]]] = None,
    model_labels: Optional[Dict[str, Dict[str, str]]] = None,
    figsize: Optional[Tuple[int, int]] = None,
    output_filename: Optional[str] = None,
    show_plot: bool = True,
    show_grid: bool = True,
    alpha: float = 0.5,
    frontier_color: str = "black",
    frontier_linewidth: float = 2.5,
):
    """
    Plot Pareto frontier visualizations for multiple tasks in subplots.
    
    Creates a figure with one panel per task, each showing the exploration
    cloud + Pareto frontier. Supports multiple models per task.
    
    Parameters:
    -----------
    models_dict : Dict[str, any]
        Dictionary mapping task names to dspy models with detailed_results.candidates.
        If models_per_task is provided, this is ignored.
    tasks_dict : Dict[str, any]
        Dictionary mapping task names to task objects with compute_privacy and compute_utility
    test_set_size : int
        Number of test examples to use for evaluation (default: 10)
    candidate_set_size : int
        Maximum number of candidates to evaluate per model (default: 10)
    models_per_task : Optional[Dict[str, Dict[str, any]]]
        Dictionary mapping task names to dictionaries of model names -> models.
        If provided, multiple models per task will be plotted with different colors/shapes.
    model_labels : Optional[Dict[str, Dict[str, str]]]
        Optional dictionary mapping task names to model name -> display label mappings
    figsize : Optional[Tuple[int, int]]
        Figure size. If None, automatically determined based on number of tasks
    output_filename : Optional[str]
        If provided, saves the plot to this filename
    show_plot : bool
        If True, calls plt.show()
    show_grid : bool
        If True, displays grid
    alpha : float
        Transparency of scatter points (default: 0.5)
    frontier_color : str
        Color for Pareto frontier line (default: "black")
    frontier_linewidth : float
        Line width for Pareto frontier (default: 2.5)
    
    Returns:
    --------
    fig, axes : matplotlib figure and axes objects
    
    Example:
    --------
    # Single model per task:
    models_dict = {
        "DB-Bio": dspy.load("trained_models/dbbio/mistral_small/dynamic/", allow_pickle=True),
        "PUPA": dspy.load("trained_models/pupa/mistral_small/dynamic/", allow_pickle=True),
    }
    tasks_dict = {
        "DB-Bio": dbbio_task,
        "PUPA": pupa_task,
    }
    
    # Multiple models per task:
    models_per_task = {
        "DB-Bio": {
            "Model1": dspy.load("./programs/dbbio/model1/", allow_pickle=True),
            "Model2": dspy.load("./programs/dbbio/model2/", allow_pickle=True),
        },
        "PUPA": {
            "Model1": dspy.load("./programs/pupa/model1/", allow_pickle=True),
        },
    }
    
    fig, axes = plot_pareto_frontier_multi_task(
        models_dict=models_dict,  # or models_per_task=models_per_task
        tasks_dict=tasks_dict,
        output_filename="pareto_frontiers.png"
    )
    """
    import dspy
    import numpy as np
    
    # Default colors and markers for different models
    default_colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", 
                     "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]
    default_markers = ["o", "s", "v", "^", "D", "p", "*", "h", "X", "P"]
    
    # Determine if we have multiple models per task
    if models_per_task is not None:
        task_names = list(models_per_task.keys())
        use_multi_models = True
    else:
        task_names = list(models_dict.keys())
        use_multi_models = False
    
    n_tasks = len(task_names)
    
    if n_tasks == 0:
        raise ValueError("models_dict/models_per_task and tasks_dict must not be empty")
    
    # Determine subplot layout
    if n_tasks == 1:
        nrows, ncols = 1, 1
    elif n_tasks == 2:
        nrows, ncols = 1, 2
    elif n_tasks <= 4:
        nrows, ncols = 2, 2
    elif n_tasks <= 6:
        nrows, ncols = 2, 3
    else:
        ncols = 3
        nrows = (n_tasks + ncols - 1) // ncols
    
    if figsize is None:
        figsize = (6 * ncols, 5 * nrows)
    
    # Font configurations
    XTICK_FONT = {"fontsize": 14, "fontweight": "bold"}
    YTICK_FONT = {"fontsize": 14, "fontweight": "bold"}
    TITLE_FONT = {"fontsize": 18, "fontweight": "bold"}
    XLABEL_FONT = {"fontsize": 16, "fontweight": "bold"}
    YLABEL_FONT = {"fontsize": 16, "fontweight": "bold"}
    
    # Create figure with subplots
    fig, axes = plt.subplots(nrows, ncols, figsize=figsize)
    if n_tasks == 1:
        axes = [axes]
    else:
        axes = axes.flatten()
    
    # Process each task
    for idx, task_name in enumerate(task_names):
        ax = axes[idx]
        task = tasks_dict[task_name]
        
        # Create evaluator with test set
        evaluator = dspy.Evaluate(
            devset=task.examples_test[:test_set_size],
            num_threads=8,
            display_progress=False,
            provide_traceback=False,
        )
        
        # Get models for this task
        if use_multi_models:
            task_models_dict = models_per_task[task_name]
        else:
            # Single model per task
            task_models_dict = {task_name: models_dict[task_name]}
        
        model_names = list(task_models_dict.keys())
        n_models = len(model_names)
        
        # Collect all scores from all models for this task
        all_scores = []
        model_info = []
        total_candidates = 0
        
        for model_idx, model_name in enumerate(model_names):
            model_obj = task_models_dict[model_name]
            
            # Extract candidates
            candidates = model_obj.detailed_results.candidates[:candidate_set_size]
            n_candidates = len(candidates)
            
            if n_candidates == 0:
                print(f"Warning: No candidates found for {task_name}/{model_name}")
                continue
            
            total_candidates += n_candidates
            
            # Evaluate all candidates
            print(f"\n[{task_name}/{model_name}] Evaluating {n_candidates} candidates on {test_set_size} test examples...")
            for i, candidate in enumerate(candidates):
                privacy_result = evaluator(candidate, metric=task.compute_privacy)
                utility_result = evaluator(candidate, metric=task.compute_utility)
                all_scores.append({
                    "privacy": privacy_result.score,
                    "utility": utility_result.score,
                })
                model_info.append(model_idx)
                if (i + 1) % 10 == 0:
                    print(f"  Evaluated {i + 1}/{n_candidates} candidates...")
        
        if len(all_scores) == 0:
            print(f"Warning: No candidates found for {task_name}")
            ax.text(0.5, 0.5, f"No candidates\nfor {task_name}", 
                   ha="center", va="center", transform=ax.transAxes, fontsize=16)
            ax.set_title(task_name, fontdict=TITLE_FONT)
            continue
        
        # Convert to arrays
        privacy_scores = np.array([s["privacy"] for s in all_scores])
        utility_scores = np.array([s["utility"] for s in all_scores])
        model_indices = np.array(model_info)
        
        # Compute Pareto frontier across all models for this task
        pareto_indices = compute_pareto_frontier(privacy_scores, utility_scores)
        n_pareto = len(pareto_indices)
        
        print(f"[{task_name}] Found {n_pareto} non-dominated solutions on the Pareto frontier")
        
        # Store handles for legend
        legend_handles = []
        
        # Plot candidates for each model with different colors and shapes
        for model_idx, model_name in enumerate(model_names):
            # Get color and marker for this model
            color = default_colors[model_idx % len(default_colors)]
            marker = default_markers[model_idx % len(default_markers)]
            
            # Get label
            if model_labels and task_name in model_labels and model_name in model_labels[task_name]:
                label = model_labels[task_name][model_name]
            else:
                label = model_name
            
            # Filter scores for this model
            model_mask = model_indices == model_idx
            model_privacy = privacy_scores[model_mask]
            model_utility = utility_scores[model_mask]
            
            if len(model_privacy) > 0:
                # Plot convex hull (exploration region) if we have at least 3 points
                if len(model_privacy) >= 3:
                    try:
                        points = np.column_stack((model_privacy, model_utility))
                        hull = ConvexHull(points)
                        # Plot filled region
                        for simplex in hull.simplices:
                            ax.fill(
                                points[simplex, 0],
                                points[simplex, 1],
                                color=color,
                                alpha=0.15,
                                edgecolor=None,
                                zorder=1,
                            )
                        # Plot hull outline
                        hull_points = points[hull.vertices]
                        ax.plot(
                            np.append(hull_points[:, 0], hull_points[0, 0]),
                            np.append(hull_points[:, 1], hull_points[0, 1]),
                            color=color,
                            linewidth=1.5,
                            alpha=0.4,
                            linestyle="-",
                            zorder=2,
                        )
                    except:
                        # If convex hull fails (e.g., collinear points), skip region
                        pass
                
                # Plot scatter points
                scatter = ax.scatter(
                    model_privacy,
                    model_utility,
                    c=color,
                    marker=marker,
                    alpha=alpha,
                    s=40,
                    edgecolors="black",
                    linewidths=0.3,
                    label=label,
                    zorder=3,
                )
                legend_handles.append(scatter)
        
        # Plot Pareto frontier line
        if n_pareto > 0:
            pareto_privacy = privacy_scores[pareto_indices]
            pareto_utility = utility_scores[pareto_indices]
            
            # Draw connected line for Pareto frontier
            ax.plot(
                pareto_privacy,
                pareto_utility,
                color=frontier_color,
                linewidth=frontier_linewidth,
                linestyle="--",
                alpha=0.8,
                zorder=4,
            )
        
        # Set title and labels
        ax.set_title(f"{task_name}\n(n={total_candidates}, frontier={n_pareto})", fontdict=TITLE_FONT)
        ax.set_xlabel("Privacy Score", fontdict=XLABEL_FONT)
        ax.set_ylabel("Utility Score", fontdict=YLABEL_FONT)
        
        # Set tick label fonts
        ax.tick_params(axis="x", labelsize=XTICK_FONT["fontsize"], width=1)
        ax.tick_params(axis="y", labelsize=YTICK_FONT["fontsize"], width=1)
        
        for label in ax.get_xticklabels():
            label.set_fontweight(XTICK_FONT["fontweight"])
        for label in ax.get_yticklabels():
            label.set_fontweight(YTICK_FONT["fontweight"])
        
        # Add legend
        if len(legend_handles) > 0:
            LEGEND_FONT = FontProperties(family="sans-serif", size=12, weight="bold")
            ax.legend(
                handles=legend_handles,
                prop=LEGEND_FONT,
                title_fontproperties=LEGEND_FONT,
                framealpha=1.0,
                loc="best",
            )
        
        # Add grid if requested
        if show_grid:
            ax.grid(alpha=0.3)
    
    # Hide unused subplots
    for idx in range(n_tasks, len(axes)):
        axes[idx].axis("off")
    
    plt.tight_layout()
    
    # Save if filename provided
    if output_filename:
        plt.savefig(output_filename, dpi=300, bbox_inches="tight")
        print(f"\nPlot saved to {output_filename}")
    
    # Show plot if requested
    if show_plot:
        plt.show()
    
    return fig, axes


# Example usage:
if __name__ == "__main__":
    # Sample data
    data_series = [
        {
            "x": [10, 20, 30, 40, 50],
            "y": [65, 70, 68, 75, 78],
            "label": "GEPA",
            "color": "black",
        },
        {
            "x": [10, 20, 30, 40, 50],
            "y": [60, 72, 74, 76, 80],
            "label": "GEPA_Rich",
            "color": "red",
        },
    ]

    fig, ax = plot_optimization_results(
        data_series=data_series,
        title="TAB, Mistral-small",
        xlabel="Number of Rollouts",
        ylabel="Score",
        output_filename="example_plot.png",
    )
