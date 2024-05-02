**The difference
{% if s.p_value <= s.alpha %}
 is
{% else %}
 is not
{% endif %}
 statistically significant.**

Since the p-value is
{% if s.p_value <= s.alpha %}
 smaller than or equal to
{% else %}
 larger than
{% endif %}
 alpha, the null hypothesis
{% if s.p_value <= s.alpha %}
 is
{% else %}
 fails to be
{% endif %}
 rejected. The observed difference of
{% if i.test == "Proportions" %}
 {{ (100 * s.observed_diff)|prettify_number(sign="+") }} p.p. ({{ (100 * s.observed_diff / s.control_prop)|prettify_number(sign="+") }}%),
{% elif i.test == "Means" %}
 {{ s.observed_diff|prettify_number(sign="+") }} ({{ (100 * s.observed_diff / s.control_mean)|prettify_number(sign="+") }}%),
{% endif %}
 between the control and the treatment groups,
{% if s.p_value <= s.alpha %}
 is
{% else %}
 is not
{% endif %}
 significant at a {{ (100 * i.confidence)|int }}% confidence level.
