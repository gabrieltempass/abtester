**Control**$\\$
Users: {{ s.control_n|prettify_number(0) }}$\\$
Mean: {{ s.control_mean|prettify_number }}$\\$
Standard deviation: {{ s.control_std|prettify_number }}

**Observed difference**$\\$
{{ s.observed_diff|prettify_number }} ({{ (100 * s.observed_diff / s.control_mean)|prettify_number(sign="+") }}%)

{% if i.method != "Permutation" %}
**Test statistic**$\\$
{{ s.tstat|prettify_number(4) }}
{% endif %}

{% if i.method == "t-test" %}
**Degrees of freedom**$\\$
{{ s.dof|prettify_number(0) }}
{% endif %}
