# Bass Diffusion Analysis of Apple AirPods Pro 3

## 1. Selected Innovation

I have selected **Apple AirPods Pro 3** from TIME's Best Inventions of 2025 list.

This project applies the Bass Diffusion Model to estimate how AirPods Pro 3 may diffuse through the global market over time. Because AirPods Pro 3 are a new product, there is not yet a sufficiently long historical adoption series for the product itself. Therefore, historical worldwide sales of the Apple AirPods product family are used as a look-alike innovation to estimate the diffusion parameters.

## 2. Historical Look-Alike Innovation

The historical look-alike used in this analysis is the **Apple AirPods product family**. This is a suitable analogue because both the historical AirPods family and AirPods Pro 3 belong to the same true wireless earbud ecosystem and share the same basic functionality: compact wireless audio, portability, and close integration with Apple devices.

AirPods Pro 3 has advanced functionality, including heart-rate sensing, improved noise cancellation, hearing-health features, and Live Translation. However, the underlying adoption process is still similar: consumers decide whether to adopt a premium wireless-earbud product, and later adopters may be influenced by product visibility, reviews, word of mouth, and the broader Apple ecosystem.

The comparison is not perfect because AirPods Pro 3 is a later-generation product in an already established category, while the earlier AirPods family helped develop the category itself. Therefore, the historical AirPods diffusion parameters are used as an illustrative benchmark rather than an assumption that AirPods Pro 3 will repeat the historical pattern exactly.

## 3. Historical Data

The historical dataset contains **worldwide Apple AirPods unit sales from 2017 to 2025**, measured in millions of units.

The source of the historical series is **Statista: “Unit sales of the Apple AirPods worldwide from 2017 to 2025 (in millions)”**.

Annual unit sales are used as a proxy for adoption. however, this is an important limitation because unit sales are not identical to unique first-time adopters: a customer can replace an older pair or buy more than one pair.

## 4. Historical Sales Pattern

The historical data show rapid growth from 2017 to 2020, when annual sales reached 114 million units. After 2020, sales declined overall, although they increased again in 2025.

This pattern broadly resembles a diffusion process: an early growth phase followed by a slowdown. However, actual yearly sales are affected by many factors other than diffusion, including product launches, replacement purchases, competition, pricing, and market conditions.

## 5. Bass Diffusion Model

Coming to the Bass Diffusion Model it is explained by the followings:

- **Innovation effect (p):** adoption that occurs independently of previous adopters, they just want to try the new product.
- **Imitation effect (q):** adoption influenced by existing adopters, for example through reviews, social influence, word of mouth, or visibility of the product.


## 6. Parameter Estimation from Historical AirPods Sales

The Bass parameters were estimated using nonlinear least squares in Python. The historical AirPods unit-sales series was fitted to the Bass sales function.

The estimated parameters are:
m = 758.06 million units

p = 0.0289

 q = 0.4296


The estimated imitation coefficient is much larger than the innovation coefficient. This suggests that the historical diffusion of AirPods was influenced more strongly by imitation and social influence than by independent adoption.

The estimated m of approximately 758 million units refers to the historical AirPods sales series. It is not automatically assumed to be the market potential of AirPods Pro 3.


## 7. Scope of the Forecast

The forecast is conducted at the **global level**.

A global level is appropriate because AirPods Pro 3 are sold internationally and are part of Apple's worldwide ecosystem. 

## 8. Fermi Estimate of AirPods Pro 3 Market Potential

Because AirPods Pro 3 are new, their final market potential cannot be directly observed. So we use Fermi estimate.

Apple has reported an installed base of more than **2.5 billion active devices worldwide**. We assume that approximately **20%** of that installed base could represent potential buyers of AirPods Pro 3.


Thus, the assumed market potential for the AirPods Pro 3 forecast is **500 million units**.

The 20% value is an assumption rather than an observed market statistic. It is used as a transparent Fermi estimate because the final potential market for AirPods Pro 3 is not yet known.

## 9. Estimated AirPods Pro 3 Adopters Over Time

The forecast begins in 2026 and covers 15 years.

| Year | New adopters (millions) | Cumulative adopters (millions) |
|---|---:|---:|
| 2026 | 21.27 | 21.27 |
| 2027 | 30.17 | 51.44 |
| 2028 | 40.62 | 92.06 |
| 2029 | 51.01 | 143.08 |
| 2030 | 58.71 | 201.78 |
| 2031 | 61.13 | 262.91 |
| 2032 | 57.35 | 320.26 |
| 2033 | 48.79 | 369.05 |
| 2034 | 38.18 | 407.23 |
| 2035 | 27.98 | 435.21 |
| 2036 | 19.54 | 454.75 |
| 2037 | 13.19 | 467.94 |
| 2038 | 8.70 | 476.64 |
| 2039 | 5.65 | 482.29 |
| 2040 | 3.64 | 485.92 |

The forecast shows the typical Bass diffusion pattern. New adoption increases during the early years, reaches its highest level around **2031**, and then declines as the potential market becomes increasingly saturated. Cumulative adoption continues increasing over time and gradually approaches the assumed market potential.

## 10. Interpretation

The model suggests that AirPods Pro 3 adoption would grow gradually at first and then speed up as more people start using the product. Since q is much larger than p, the model indicates that word of mouth, reviews, and the influence of existing users are likely to matter more than purely independent adoption.

With an assumed market potential of 500 million units, the model predicts that new adoption would reach its highest point at around 61 million units in 2031. After that, the number of new adopters would start to fall because a large part of the potential market would already have adopted the product.

These results should be treated as an estimate rather than an exact forecast. They depend on the assumption that AirPods Pro 3 will follow a similar adoption pattern to earlier AirPods and that the 500 million market potential is a reasonable approximation.

## 11. Limitations

There are a few limitations to this analysis. First, the historical data represent AirPods unit sales rather than the number of unique new adopters. Some customers may have replaced an older pair or bought more than one pair, so sales are only an approximation of adoption.

The historical dataset is also relatively short, covering only the years from 2017 to 2025. In addition, AirPods Pro 3 are entering an already established wireless-earbuds market, while the earlier AirPods data include the period when this product category was still growing quickly.

Finally, the assumed market potential of 500 million units is a Fermi estimate rather than an observed value. The forecast also assumes that AirPods Pro 3 will follow a similar diffusion pattern to earlier AirPods. In reality, future adoption may also be affected by factors such as price, competition, new product releases, and changes in customer preferences.

## 12. Conclusion

This project uses historical worldwide AirPods sales as a similar past innovation to estimate the Bass diffusion parameters for AirPods Pro 3. Based on the historical data, the estimated innovation coefficient is p=0.0289, the imitation coefficient is q=0.4296, and the historical market potential is approximately 758 million units.

To forecast the diffusion of AirPods Pro 3, the estimated p and q values were kept the same, while a separate market potential of 500 million units was assumed using a Fermi-style estimate. Under these assumptions, the number of new adopters increases during the first few years, reaches its highest point around 2031, and then gradually decreases as more of the potential market has already adopted the product.

Overall, the analysis shows how the Bass model can be used to make a reasonable forecast for a new product by learning from the adoption pattern of a similar product, especially when long-term data for the new innovation are not yet available.

## References

1. TIME. *Best Inventions of 2025: Apple AirPods Pro 3.* https://time.com/collections/best-inventions-2025/7318483/apple-airpods-pro-3/
2. Statista. *Unit sales of the Apple AirPods worldwide from 2017 to 2025 (in millions).*(https://www.statista.com/statistics/1421624/apple-airpods-unit-sales/)
3. Apple. Apple Newsroom / investor reporting on the worldwide active-device installed base. The project uses the reported figure of more than 2.5 billion active devices as the basis for the Fermi estimate.
4. Hovhannisyan, K. *DS 223 Marketing Analytics — Bass Model for Innovation Diffusion.
