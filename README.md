# my-conditional-beta-analysis
This project investigates the asymmetric behavior of asset betas under different market conditions. Instead of assuming a constant beta as in the standard CAPM, the analysis estimates β⁺ (up-market beta) and β⁻ (down-market beta) to capture how sensitivity to the S&amp;P 500 varies depending on whether the market is rising or falling.
# Conditional Beta Analysis on the S&P 500  

This project studies **time-varying risk exposure** by estimating **conditional betas** for S&P 500 constituents across multiple sectors. Instead of a constant beta as in the CAPM, it separates market sensitivity into:  

- **β⁺ (up-market beta):** exposure when the S&P 500 return is positive  
- **β⁻ (down-market beta):** exposure when the S&P 500 return is negative  

This approach highlights the **asymmetry of risk**: some stocks and sectors react more strongly to downturns than upturns, while others behave in the opposite way.  

---

## Methodology  
1. **Data**  
   - Daily stock prices for 45 large-cap U.S. companies (Energy, Financials, Tech, etc.)  
   - Benchmark: S&P 500 (^GSPC)  
   - Source: Yahoo Finance (`yfinance` API)  

2. **Returns Calculation**  
   - Compute daily percentage returns for each ticker and the S&P 500.  

3. **Conditional Beta Estimation**  
   - For each stock, split market returns into **up** (Rₘ > 0) and **down** (Rₘ < 0) days.  
   - Estimate β⁺ and β⁻ via covariance with the market.  
   - Compute **β Ratio = β⁺ / β⁻** as a measure of asymmetry.  

4. **Visualization**  
   - Average β⁺ and β⁻ by sector  
   - β⁺/β⁻ ratio heatmaps  
   - Top 5 companies per sector by conditional betas  

---

## 🔧 Technologies  
- **Python** (pandas, numpy)  
- **Data**: Yahoo Finance (`yfinance`)  
- **Visualization**: Plotly (interactive graphs)  

---

## Results & Insights  

The analysis reveals strong evidence that **stock betas are not constant** but instead vary significantly depending on market conditions. By splitting exposure into **β⁺ (up-market)** and **β⁻ (down-market)**, several key insights emerge:  

1. **Sector-Level Asymmetry**  
   - **Cyclical sectors** such as **Information Technology, Financials, and Consumer Discretionary** exhibit much higher β⁺ than β⁻.  
     - This indicates that these sectors **gain disproportionately in bull markets**, amplifying upside movements of the S&P 500.  
   - Conversely, **defensive sectors** like **Utilities and Consumer Staples** show relatively balanced or even higher β⁻ values.  
     - This reflects their tendency to **hold value during downturns**, but participate less in rallies.  
   - These findings are consistent with evidence that cyclical firms carry higher conditional market exposure than defensive firms (Ang & Chen, 2002).  

2. **β Ratio as a Risk/Opportunity Measure**  
   - The **β⁺/β⁻ ratio** provides a compact measure of asymmetry.  
     - Ratios **well above 1** highlight sectors/stocks that are **momentum-driven**, thriving in rising markets but vulnerable in downturns.  
     - Ratios **close to or below 1** identify **stable or defensive plays** that limit downside risk.  
   - For example, Technology stocks like **NVIDIA (NVDA)** and **Meta (META)** show high β ratios, confirming their growth-driven volatility profile.  

3. **Top Companies Within Sectors**  
   - Within each sector, the top 5 companies by conditional beta highlight **leaders and laggards in risk exposure**.  
   - Energy firms such as **ExxonMobil (XOM)** and **Chevron (CVX)** display strong β⁺ during commodity upswings but lower β⁻, reflecting their asymmetric exposure to oil prices and macro cycles.  
   - Healthcare firms like **Johnson & Johnson (JNJ)** and **Pfizer (PFE)** show more balanced betas, consistent with their defensive reputation.  

4. **Market Implications**  
   - **Portfolio Construction:** Incorporating conditional betas allows investors to build strategies that explicitly account for downside sensitivity. For instance, overweighting high-β⁺ stocks enhances returns in bull markets but increases crash risk.  
   - **Risk Management:** Stress testing with β⁻ values highlights which holdings are most vulnerable during downturns. This is particularly relevant for hedge funds and risk-parity strategies.  
   - **Factor Investing:** The β ratio can be interpreted as a factor capturing **asymmetry in risk exposure**, which could be integrated into multi-factor models alongside size, value, and momentum (Petkova & Zhang, 2005).  

5. **Statistical Significance**  
   - Across the dataset, the difference between β⁺ and β⁻ is **statistically significant in most sectors**, confirming that the asymmetry is not random noise but a structural feature of market dynamics.  
   - This result aligns with academic literature on **downside risk and conditional CAPM**, which argues that investors demand higher premiums for assets that underperform in bear markets (Ang, Chen, & Xing, 2006).  

**Conclusion:**  
The conditional beta framework provides a **richer, more realistic picture of systematic risk** than the static CAPM. By separating β⁺ and β⁻, this project highlights how sensitivity to the S&P 500 is **state-dependent**, offering valuable insights for both asset pricing research and practical portfolio management.  

---

### 📚 References  
- Ang, A., & Chen, J. (2002). *Asymmetric correlations of equity portfolios*. Journal of Financial Economics, 63(3), 443–494.  
- Petkova, R., & Zhang, L. (2005). *Is value riskier than growth?*. Journal of Financial Economics, 78(1), 187–202.  
- Ang, A., Chen, J., & Xing, Y. (2006). *Downside risk*. The Review of Financial Studies, 19(4), 1191–1239.    

---

## 📂 Repository Structure  
