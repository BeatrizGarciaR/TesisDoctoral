# 900 demand points, 50 potential sites, 100 scenarios
amb = rbind(c(10, 6), c(20, 11), c(35,20))
len_I <- c(900)
len_L <- c(50)
len_S <- c(100)

#objective
aux_0 <- as.data.frame(read.csv(paste('Tesis_Obj_Zs_090424_AllAmb.csv', sep="")))

aux <- as.data.frame(aux_0[1:3, c(11,12,6)])
aux_bb <- as.data.frame(aux_0[1:3, c(11,12,7)])

pdf(paste("Objective_ObjZs_Scenarios_090424_AllAmb.pdf", sep=""), width = 10)
par(mfrow = c(1, 1), mar=c(5.5, 5, 7.1, 1.9))
plot(aux[,3], pch=15, col=1, cex=1.5, ylim=c(0,max(aux)+15),
     cex.lab=2.7, cex.axis = 2.5, xlab="ambulances [BLS, ALS]", ylab="objective value",
     xaxt= "n", tck = 0.02) #ann = FALSE,
title(paste("900 demand points, 100 scenarios \n and 50 potential sites", sep=" "), cex.main = 3.5)
axis(1, at=1:3, labels=c("[10, 6]", "[20, 11]", "[35, 20]"), cex.axis = 2.5, tck = 0.02)
lines(aux[,3], lwd=3, col=1)
points(aux_bb[,3], pch=15, cex=1.5, col=2)
lines(aux_bb[,3], lwd=3, col=2, lty=2)
legend(x = "left",         # Posición
       legend = c("best objective", "best bound"), # Textos de la leyenda
       lty = c(1, 2),          # Tipo de líneas
       col = c(1, 2),          # Colores de las líneas
       lwd = 2, bty = "n", cex = 2.2)
dev.off()

# time 
aux_time <- as.data.frame(aux_0[1:3, c(11,12,10)])

pdf(paste("Timeval_ObjZs_Scenarios_090424_AllAmb.pdf", sep=""), width = 10)
par(mfrow = c(1, 1), mar=c(5.5, 5, 7.1, 1.9))
plot(aux_time[,3], pch=15, col=1, cex=1.5, ylim=c(0,15000),
     cex.lab=2.7, cex.axis = 2.5, xlab="ambulances [BLS, ALS]", ylab="runtime in seconds",
     xaxt= "n", tck = 0.02) #ann = FALSE,
title(paste("900 demand points, 100 scenarios \n and 50 potential sites", sep=" "), cex.main = 3.5)
axis(1, at=1:3, labels=c("[10, 6]", "[20, 11]", "[35, 20]"), cex.axis = 2.5, tck = 0.02)
lines(aux_time[,3], lwd=3, col=1)
dev.off()

# #coverage 
# for (a in 1:length(amb[,1])){
#   eta <- amb[a,]
#   accidents_covered <- data.frame()
#   for (i in 1:length(len_I)){
#     for (l in 1:length(len_L)){
#       for (s in 1: length(len_S)){
#         accidents <- suppressWarnings(as.data.frame(read.table(paste('Accidents_ObjZs_Scenarios_090424_', len_I[i], '_', len_L[l], '_', len_S[s], '.txt', sep=""))))
#         print(paste('Accidents_ObjZs_Scenarios_090424_', len_I[i], '_', len_L[l], '_', len_S[s], '.txt', sep=""))
#         datos <- c()
#         datos <- cbind(datos, len_I[i], len_L[l], len_S[s])
#         
#         full <- as.data.frame(read.table(paste('Full_ObjZs_Scenarios_090424_', len_I[i], '_', len_L[l], '_', len_S[s], '_',eta[1],'_',eta[2],'.txt', sep="")))
#         full_expected <- matrix(ncol=len_S[s], nrow=1)
#         for (scenario in 1:len_S[s]){
#           total_full = 0
#           for (j in 1:length(full[,1])){
#             if (full[j,2] == scenario && full[j,4] == 1){
#               total_full = total_full + 1
#             }
#           }
#           full_expected_s = total_full/as.integer(accidents[scenario])
#           #print(full_expected_s)
#           full_expected[1, scenario] = full_expected_s
#         }
#         datos <- cbind(datos, prom_full_expected = mean(full_expected)*100)
#         
#         
#         partial1 <- as.data.frame(read.table(paste('Partial1_ObjZs_Scenarios_090424_', len_I[i], '_', len_L[l], '_', len_S[s], '_',eta[1],'_',eta[2],'.txt', sep="")))
#         partial1_expected <- matrix(ncol=len_S[s], nrow=1)
#         for (scenario in 1:len_S[s]){
#           total_partial1 = 0
#           for (j in 1:length(partial1[,1])){
#             if (partial1[j,2] == scenario && partial1[j,4] == 1){
#               total_partial1 = total_partial1 + 1
#             }
#           }
#           partial1_expected_s = total_partial1/as.integer(accidents[scenario])
#           #print(partial1_expected_s)
#           partial1_expected[1, scenario] = partial1_expected_s
#         }
#         datos <- cbind(datos, prom_partial1_expected = mean(partial1_expected)*100)
#         
#         
#         partial2 <- as.data.frame(read.table(paste('Partial2_ObjZs_Scenarios_090424_', len_I[i], '_', len_L[l], '_', len_S[s], '_',eta[1],'_',eta[2],'.txt', sep="")))
#         partial2_expected <- matrix(ncol=len_S[s], nrow=1)
#         for (scenario in 1:len_S[s]){
#           total_partial2 = 0
#           for (j in 1:length(partial2[,1])){
#             if (partial2[j,2] == scenario && partial2[j,4] == 1){
#               total_partial2 = total_partial2 + 1
#             }
#           }
#           partial2_expected_s = total_partial2/as.integer(accidents[scenario])
#           #print(partial2_expected_s)
#           partial2_expected[1, scenario] = partial2_expected_s
#         }
#         datos <- cbind(datos, prom_partial2_expected = mean(partial2_expected)*100)
#         
#         
#         partial3 <- as.data.frame(read.table(paste('Partial3_ObjZs_Scenarios_090424_', len_I[i], '_', len_L[l], '_', len_S[s], '_',eta[1],'_',eta[2],'.txt', sep="")))
#         partial3_expected <- matrix(ncol=len_S[s], nrow=1)
#         for (scenario in 1:len_S[s]){
#           total_partial3 = 0
#           for (j in 1:length(partial3[,1])){
#             if (partial3[j,2] == scenario && partial3[j,4] == 1){
#               total_partial3 = total_partial3 + 1
#             }
#           }
#           partial3_expected_s = total_partial3/as.integer(accidents[scenario])
#           #print(partial3_expected_s)
#           partial3_expected[1, scenario] = partial3_expected_s
#         }
#         datos <- cbind(datos, prom_partial3_expected = mean(partial3_expected)*100)
#         
#         
#         null <- as.data.frame(read.table(paste('Null_ObjZs_Scenarios_090424_', len_I[i], '_', len_L[l], '_', len_S[s], '_',eta[1],'_',eta[2],'.txt', sep="")))
#         null_expected <- matrix(ncol=len_S[s], nrow=1)
#         for (scenario in 1:len_S[s]){
#           total_null = 0
#           for (j in 1:length(null[,1])){
#             if (null[j,2] == scenario && null[j,4] == 1){
#               total_null = total_null + 1
#             }
#           }
#           null_expected_s = total_null/as.integer(accidents[scenario])
#           #print(null_expected_s)
#           null_expected[1, scenario] = null_expected_s
#         }
#         datos <- cbind(datos, prom_null_expected = mean(null_expected)*100)
#         accidents_covered <- rbind(accidents_covered, datos)
#       }
#     }
#   }
#   colnames(accidents_covered) <- c("I", "L", "S", "% Full accident coverage", "% Partial1 accident coverage", "% Partial2 accident coverage", "% Partial3 accident coverage", "% Null accident coverage")
#   write.csv(accidents_covered, file = paste('ExpectedCoverage_ObjZs_Scenarios_090424_', eta[1],'_',eta[2],'.csv', sep=""), col.names=TRUE, row.names=FALSE, dec = ".")
#   aux <- cbind(accidents_covered, eta[1], eta[2])
#   colnames(aux) <- c("I", "L", "S", "% Full accident coverage", "% Partial1 accident coverage", "% Partial2 accident coverage", "% Partial3 accident coverage", "% Null accident coverage", "BLS ambulances", "ALS ambulances")
#   accidents_covered_total <- rbind(accidents_covered_total, aux)
# }
# write.csv(accidents_covered_total, file = paste('ExpectedCoverageTotal_ObjZs_Scenarios_090424_','.csv', sep=""), col.names=TRUE, row.names=FALSE, dec = ".")


#coverage mean scenarios graphics
pdf(paste("Coverage_Obj_Zs_Scenarios_090424_AllAmb.pdf", sep=""), width = 10)
par(mfrow = c(1,1), mar=c(5.5, 5, 7.1, 1.9))

#pdf(paste("Coverage_",eta[1],"_",eta[2],".pdf", sep=""))
plot(as.numeric(accidents_covered_total[1,4:8]), pch=15, col=1, cex=1.5, ylim=c(0,100),
       cex.lab=2.7, cex.axis = 2.5, xlab="coverage type", ylab="% accidents coverage",
       xaxt= "n", tck = 0.02) #ann = FALSE,
title(paste("900 demand points, 100 scenarios \n and 50 potential sites", sep=" "), cex.main = 3.5)

axis(1, at=1:5, labels=c("Full", "Partial1", "Partial2", "Partial3", "Null"), cex.axis = 2.5, tck = 0.02)
# plot(as.numeric(prom_coverage[a*5-4, 5:9]), pch=15, col=1, cex=1.5,
#      ylim=c(0, 100), ylab="% accidents coverage", xlab = "Coverage type", xaxt = "n",
#      main=paste("Mean coverage percentage for 16 potential sites \n considering",eta[1],
#                 "BLS and",eta[2],"ALS ambulances", sep=" "))
#
# axis(1, at=1:5, labels=c("Full", "Partial1", "Partial2", "Partial3", "Null"))
lines(as.integer(accidents_covered_total[1,4:8]), lwd=3, col=1)
points(as.integer(accidents_covered_total[2,4:8]), pch=16, cex=1.5, col=2)
lines(as.integer(accidents_covered_total[2,4:8]), lwd=3, col=2)
points(as.integer(accidents_covered_total[3,4:8]), pch=17, cex=1.5, col=3)
lines(as.integer(accidents_covered_total[3,4:8]), lwd=3, col=3)
legend(x="top", legend = c("[10, 6]", "[20, 11]", "[35, 20]"), horiz=TRUE,
       fill = c(1, 2, 3), title = "Ambulances [BLS, ALS]",bty = "n", cex = 2.2)
# legend(x="topleft", legend = len_I, cex=0.75, fill = c(1, 2, 3, 4, 6),
#        title = "Demand points", bty="n")
# dev.off()

dev.off()