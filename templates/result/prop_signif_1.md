**Control**$\\$
Proportion: {{ (100 * s.control_prop)|prettify_number }}%$\\$

**Observed difference**$\\$
{{ (100 * s.observed_diff)|prettify_number(sign="+") }} p.p. ({{ (100 * s.observed_diff / s.control_prop)|prettify_number(sign="+") }}%)

{% if i.method != "Permutation" %}
**Test statistic**$\\$
{{ s.tstat|prettify_number(4) }}
{% endif %}
