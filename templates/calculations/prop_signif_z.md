First, the test statistic must be calculated, with the following equation:

$$
Z = \frac{(\hat{p_t} - \hat{p_c}) - (p_t - p_c)}{\sqrt{\hat{p}(1 - \hat{p})\Big(\frac{1}{n_t} + \frac{1}{n_c}\Big)}}
$$

Note that $p_t - p_c$ is the difference between the proportions under the null hypothesis, which in this case is assumed to be zero. While the pooled proportion comes from:

$$
\hat{p} = \frac{n_t \hat{p_t} + n_c \hat{p_c}}{n_t + n_c}
$$

Thus, the equation becomes:

$$
Z = \frac{\hat{p_t} - \hat{p_c}}{\sqrt{\Big(\frac{n_t \hat{p_t} + n_c \hat{p_c}}{n_t + n_c}\Big)\Big(1 - \frac{n_t \hat{p_t} + n_c \hat{p_c}}{n_t + n_c}\Big)\Big(\frac{1}{n_t} + \frac{1}{n_c}\Big)}}
$$

Where:$\\$
$\hat{p_t}$ = Sample proportion from the treatment.$\\$
$\hat{p_c}$ = Sample proportion from the control.$\\$
$p_t$ = Population proportion from the treatment.$\\$
$p_c$ = Population proportion from the control.$\\$
$\hat{p}$ = Pooled proportion.$\\$
$n_t$ = Number of subjects in the treatment.$\\$
$n_c$ = Number of subjects in the control.

As for the solution:

$$
Z = \frac{ {{ s.treatment_prop|prettify_number(4) }} - {{ s.control_prop|prettify_number(4) }} }{\sqrt{\Big(\frac{ {{ i.treatment_users|int }} \; {{ s.treatment_prop|prettify_number(4) }} + {{ i.control_users|int }} \; {{ s.control_prop|prettify_number(4) }} }{ {{ i.treatment_users|int }} + {{ i.control_users|int }} }\Big)\Big(1 - \frac{ {{ i.treatment_users|int }} \; {{ s.treatment_prop|prettify_number(4) }} + {{ i.control_users|int }} \; {{ s.control_prop|prettify_number(4) }} }{ {{ i.treatment_users|int }} + {{ i.control_users|int }} }\Big)\Big(\frac{1}{ {{ i.treatment_users|int }} } + \frac{1}{ {{ i.control_users|int }} }\Big)}}
$$

$$
Z = {{ s.tstat|prettify_number(4, thousand_separator="") }}
$$

Once the test statistic is known, it can be used to find the p-value. Through the probability density function (PDF) of the standard Normal distribution, given by:

$$
f(x) = \frac{e^{-\frac{x^2}{2}}}{\sqrt{2 \pi}}
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
} e^{-\frac{x^2}{2}} \,\mathrm{d}x
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
} e^{-\frac{x^2}{2}} \,\mathrm{d}x
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
