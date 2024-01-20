First, the test statistic must be calculated, with the following equation:

$$
Z = \frac{(\bar{x_t} - \bar{x_c}) - (\mu_t - \mu_c)}{S_p \sqrt{\frac{1}{n_t} + \frac{1}{n_c}}}
$$

Note that $\mu_t - \mu_c$ is the difference between the means under the null hypothesis, which in this case is assumed to be zero. And the pooled standard deviation comes from:

$$
S_p = \sqrt{\frac{(n_t - 1)S_t^2 + (n_c - 1)S_c^2}{n_t + n_c - 2}}
$$

Thus, the equation becomes:

$$
Z = \frac{\bar{x_t} - \bar{x_c}}{\sqrt{\Big(\frac{(n_t - 1)S_t^2 + (n_c - 1)S_c^2}{n_t + n_c - 2}\Big)\Big(\frac{1}{n_t} + \frac{1}{n_c}}\Big)}
$$

Where:$\\$
$\bar{x_t}$ = Sample mean from the treatment.$\\$
$\bar{x_c}$ = Sample mean from the control.$\\$
$\mu_t$ = Population mean from the treatment.$\\$
$\mu_c$ = Population mean from the control.$\\$
$n_t$ = Number of subjects in the treatment.$\\$
$n_c$ = Number of subjects in the control.$\\$
$S_t$ = Standard deviation from the treatment.$\\$
$S_c$ = Standard deviation from the control.$\\$
$S_p$ = Pooled standard deviation.

As for the solution:

$$
Z = \frac{ {{ s.treatment_mean|prettify_number(4, thousand_separator="") }} - {{ s.control_mean|prettify_number(4, thousand_separator="") }} }{\sqrt{\Big(\frac{( {{ s.treatment_n }} - 1) {{ s.treatment_std|prettify_number(4, thousand_separator="") }} ^2 + ( {{ s.control_n }} - 1) {{ s.control_std|prettify_number(4, thousand_separator="") }} ^2}{ {{ s.treatment_n }} + {{ s.control_n }} - 2}\Big)\Big(\frac{1}{ {{ s.treatment_n }} } + \frac{1}{ {{ s.control_n }} }}\Big)}
$$

$$
Z = {{ s.tstat|prettify_number(4, thousand_separator="") }}
$$

Once the test statistic is known, it can be used to find the p-value. Through the probability density function (PDF) of the standard Normal distribution, given by:

$$
f(x) = \frac{e^{-x^2}}{\sqrt{2 \pi}}
$$

Since this is to test whether the alternative hypothesis is
{% if i.alternative == "smaller" %}
 smaller than
{% elif i.alternative == "larger" %}
 larger than
{% elif i.alternative == "two-sided" %}
 not equal to
{% endif %}
 the null, the p-value comes from
{% if i.alternative == "two-sided" %}
 two times
{% endif %}
{% if i.alternative == "two-sided" or i.alternative == "larger" %}
 one minus
{% endif %}
 the integral of the PDF, from minus infinity to the
{% if i.alternative == "two-sided" %}
 modulus of the
{% endif %}
 test statistic, with respect to x:

$$
p\!-\!value =
{% if i.alternative == "two-sided" %}
2 \Big(1 -
{% elif i.alternative == "larger" %}
1 -
{% endif %}
\frac{1}{\sqrt{2 \pi}}\int_{-\infty}^{
{% if i.alternative == "smaller" or i.alternative == "larger" %}
Z
{% elif i.alternative == "two-sided" %}
|Z|
{% endif %}
} e^{-x^2} \,\mathrm{d}x
{% if i.alternative == "two-sided" %}
\Big)
{% endif %}
$$

Where:$\\$
$Z$ = Test statistic.$\\$

The fraction one divided by square root of two times pi can be left out of the integral, because it is a constant that multiplies the integrand. Finally, the solution is (an online calculator, like [WolframAlpha](https://www.wolframalpha.com), could be used in this step):

$$
p\!-\!value =
{% if i.alternative == "two-sided" %}
2 \Big(1 -
{% elif i.alternative == "larger" %}
1 -
{% endif %}
\frac{1}{\sqrt{2 \pi}}\int_{-\infty}^{
{% if i.alternative == "smaller" or i.alternative == "larger" %}
{{ s.tstat|prettify_number(4, thousand_separator="") }}
{% elif i.alternative == "two-sided" %}
|{{ s.tstat|prettify_number(4, thousand_separator="") }}|
{% endif %}
} e^{-x^2} \,\mathrm{d}x
{% if i.alternative == "two-sided" %}
\Big)
{% endif %}
$$

$$
p\!-\!value
{% if s.p_value|round(4) < 0.0001 %}
< 0.0001
{% else %}
= {{ s.p_value|round(4) }}
{% endif %}
$$
