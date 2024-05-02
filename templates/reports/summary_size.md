**{{ (s.control_sample + s.treatment_sample)|prettify_number(0) }} is the minimum sample size required.**

For a true difference of at least {{ (100 * i.sensitivity)|prettify_number(1) }}% between the groups, to have a{% if i.power >= 0.8 and i.power < 0.9 %}n{% endif %} {{ (100 * i.power)|prettify_number(0) }}% probability of being detected, the experiment must have no less than a sample size of {{ s.control_sample|prettify_number(0) }} for the control and {{ s.control_sample|prettify_number(0) }} for the treatment.
