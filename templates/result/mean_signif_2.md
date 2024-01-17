**Treatment**$\\$
Users: {{ s.treatment_n|prettify_number(0) }}$\\$
Mean: {{ s.treatment_mean|prettify_number }}$\\$
Standard deviation: {{ s.treatment_std|prettify_number }}

**Alpha**$\\$
{{ s.alpha|prettify_number(4) }}

**p-value**$\\$
{% if s.p_value|round(4) < 0.0001 %}< 0.0001{% else %}{{ s.p_value|round(4) }}{% endif %}
