**The difference
{% if s.p_value <= s.alpha %}
 is
{% else %}
 is not
{% endif %}
 statistically significant.**

The p-value is
{% if s.p_value < s.alpha %}
 smaller than
{% elif s.p_value == s.alpha %}
 equal to
{% else %}
 larger than
{% endif %}
 alpha (which comes from one minus the confidence level) and the null hypothesis
{% if s.p_value <= s.alpha %}
 is
{% else %}
 fails to be
{% endif %}
 rejected.
