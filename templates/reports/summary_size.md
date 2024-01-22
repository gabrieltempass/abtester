**{{ (s.control_sample + s.treatment_sample)|prettify_number(0) }} is the minimum sample size required.**

To measure, with statistical significance, a difference of at least {{ (100 * i.sensitivity)|prettify_number(1) }}% between the groups, the experiment must have no less than a sample size of {{ s.control_sample|prettify_number(0) }} for the control and {{ s.control_sample|prettify_number(0) }} for the treatment.
