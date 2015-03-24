library(phangorn)
titv <- function(q) return(sum(q[c(2, 5)]) / sum(q[-c(2, 5)]))

out_data<- matrix(NA, 100, 8)
colnames(out_data) <- c('titv1', 'titv2', 'titv3', 'titv4',  'alpha1', 'alpha2', 'alpha3', 'alpha4')


for(i in 1:100){
    cat('SIMULATION', i, '\n')
    # Simulate tree for first partition with a total tree length of 1
    tr_1 <- rtree(10)
    tr_1$edge.length <- tr_1$edge.length /(sum(tr_1$edge.length))

    gamma_rates <- phangorn:::discrete.gamma(0.4, 4)

    q <- c(0.1, 0.8, 0.1, 0.1, 0.8, 0.1)

    s_11 <- simSeq(tr_1, l = 125, Q = q, rate = gamma_rates[1])
    s_12 <- simSeq(tr_1, l = 125, Q = q, rate = gamma_rates[2])
    s_13 <- simSeq(tr_1, l = 125, Q = q, rate = gamma_rates[3])
    s_14 <- simSeq(tr_1, l = 125, Q = q, rate = gamma_rates[4])
    s1 <- c(s_11, s_12, s_13, s_14)

fit1 <- optim.pml(pml(tr_1, s1, shape = 1, k = 4), optQ = T, optGamma = T, optBF = T)

    ## 2
tr_2 <- tr_1
    tr_2$edge.length <- tr_1$edge.length  * 5
    gamma_rates <- gamma_rates * 5
    s_21 <- simSeq(tr_2, l = 125, Q = q, rate = gamma_rates[1])
    s_22 <- simSeq(tr_2, l = 125, Q = q, rate = gamma_rates[2])
    s_23 <- simSeq(tr_2, l = 125, Q = q, rate = gamma_rates[3])
    s_24 <- simSeq(tr_2, l = 125, Q = q, rate = gamma_rates[4])
    s2 <- c(s_21, s_22, s_23, s_24)

fit2 <- optim.pml(pml(tr_2, s2, shape = 1, k = 4), optQ = T, optGamma = T, optBF = T)

## 3
tr_3 <- tr_1
    tr_3$edge.length <- tr_1$edge.length  * 10
    gamma_rates <- gamma_rates * 10
    s_31 <- simSeq(tr_3, l = 125, Q = q, rate = gamma_rates[1])
    s_32 <- simSeq(tr_3, l = 125, Q = q, rate = gamma_rates[2])
    s_33 <- simSeq(tr_3, l = 125, Q = q, rate = gamma_rates[3])
    s_34 <- simSeq(tr_3, l = 125, Q = q, rate = gamma_rates[4])
    s3 <- c(s_31, s_32, s_33, s_34)

fit3 <- optim.pml(pml(tr_3, s3, shape = 1, k = 4), optQ = T, optGamma = T, optBF = T)

## 4
tr_4 <- tr_1
    tr_4$edge.length <- tr_1$edge.length  * 15
    gamma_rates <- gamma_rates * 15
    s_41 <- simSeq(tr_4, l = 125, Q = q, rate = gamma_rates[1])
    s_42 <- simSeq(tr_4, l = 125, Q = q, rate = gamma_rates[2])
    s_43 <- simSeq(tr_4, l = 125, Q = q, rate = gamma_rates[3])
    s_44 <- simSeq(tr_4, l = 125, Q = q, rate = gamma_rates[4])
    s4 <- c(s_41, s_42, s_43, s_44)

fit4 <- optim.pml(pml(tr_4, s4, shape = 1, k = 4), optQ = T, optGamma = T, optBF = T)

## 5
#tr_5 <- tr_1
#    tr_5$edge.length <- tr_1$edge.length  * 20
#    gamma_rates <- gamma_rates * 20
#    s_51 <- simSeq(tr_5, l = 125, Q = q, rate = gamma_rates[1])
#    s_52 <- simSeq(tr_5, l = 125, Q = q, rate = gamma_rates[2])
#    s_53 <- simSeq(tr_5, l = 125, Q = q, rate = gamma_rates[3])
#    s_54 <- simSeq(tr_5, l = 125, Q = q, rate = gamma_rates[4])
#    s5 <- c(s_51, s_52, s_53, s_54)

#fit5 <- optim.pml(pml(tr_5, s5, shape = 1, k = 4), optQ = T, optGamma = T, optBF = T)



   out_data[i, ] <- c(titv(fit1$Q), titv(fit2$Q),  titv(fit3$Q), titv(fit4$Q),   fit1$shape, fit2$shape, fit3$shape, fit4$shape)

print(out_data[1:i, ])

}

write.table(out_data, file = 'simulation_results.csv', sep = ',', row.names = F)

out_data <- out_data[-c(4, 27), ]

pdf('Fig2_simulations.pdf', useDingbats = F, width = 12)
par(mfrow = c(1, 2))
plot(c(1, 5, 10, 15), out_data[1, 1:4], type = 'b', ylim = range(out_data[, 1:5]), pch = 20, col = rgb(0, 0, 0, 0.2), xlab = 'Tree length', ylab = expression(italic('ti/tv')), xlim = c(0, 16))
for(i in 2:nrow(out_data)){
    points(jitter(c(1, 5, 10, 15)), out_data[i, 1:4], type = 'b', pch = 20, col = rgb(0, 0, 0, 0.2))
}

plot(c(1, 5, 10, 15), out_data[1, 5:8], type = 'b', ylim = range(out_data[, 5:8]), pch = 20, col = rgb(0, 0, 0, 0.2), ylab = expression(italic(alpha)), xlab = '', xlim = c(0, 16))
for(i in 2:nrow(out_data)){
    points(jitter(c(1, 5, 10, 15)), out_data[i, 5:8], type = 'b', col = rgb(0, 0, 0, 0.2), pch = 20)
}
dev.off()
