**Treatment**$\\$
Proportion: {{ (100 * s.treatment_prop)|prettify_number }}%$\\$

**Alpha**$\\$
{{ s.alpha|prettify_number(4) }}

**p-value**$\\$
{% if s.p_value|round(4) < 0.0001 %}< 0.0001{% else %}{{ s.p_value|round(4) }}{% endif %}
