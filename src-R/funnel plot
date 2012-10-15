#TH: funnel plot code from:
#TH: http://stats.stackexchange.com/questions/5195/how-to-draw-funnel-plot-using-ggplot2-in-r/5210#5210
#TH: Use our cancerdata
number = PS_UcastObce$Volici

#TH: The rate is given as a 'per 100,000' value, so normalise it
p=PS_UcastObce$UcastRate

p.se <- sqrt((p*(1-p)) / (number))
df <- data.frame(p, number, p.se)

## common effect (fixed effect model)
p.fem <- weighted.mean(p, (1/(p.se)^2))

## lower and upper limits for 95% and 99.9% CI, based on FEM estimator
#TH: I'm going to alter the spacing of the samples used to generate the curves
number.seq <- seq(0, max(number), 10)
number.ll95 <- p.fem - 1.96 * sqrt((p.fem*(1-p.fem)) / (number.seq))
number.ul95 <- p.fem + 1.96 * sqrt((p.fem*(1-p.fem)) / (number.seq))
number.ll999 <- p.fem - 3.29 * sqrt((p.fem*(1-p.fem)) / (number.seq))
number.ul999 <- p.fem + 3.29 * sqrt((p.fem*(1-p.fem)) / (number.seq))
dfCI <- data.frame(number.ll95, number.ul95, number.ll999, number.ul999, number.seq, p.fem)

## draw plot
#TH: note that we need to tweak the limits of the y-axis
fp <- ggplot(aes(x = number, y = p), data = df) +
geom_point(shape = 1) +
geom_line(aes(x = number.seq, y = number.ll95), data = dfCI) +
geom_line(aes(x = number.seq, y = number.ul95), data = dfCI) +
geom_line(aes(x = number.seq, y = number.ll999), data = dfCI) +
geom_line(aes(x = number.seq, y = number.ul999), data = dfCI) +
geom_hline(aes(yintercept = p.fem), data = dfCI) +
scale_y_continuous(limits = c(0,0.0004)) +
xlab("number") + ylab("p") + theme_bw()

fp