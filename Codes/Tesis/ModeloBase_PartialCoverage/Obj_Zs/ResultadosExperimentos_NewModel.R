amb <- rbind(c(10, 6), c(20, 11), c(35,20))
#amb <- rbind(c(10,6))
# len_I <- c(168, 270, 500, 900, 1500)
# len_L <- c(16, 30, 50, 70, 100)
# len_S <- c(10, 50, 100, 150, 200)

len_I <- c(168, 270, 500, 900, 1500)
len_L <- c(16)
len_S <- c(10, 50, 100, 150, 200)


# time value graphics
counti = 0
#for (i in len_I){

for (a in 1:length(amb[,1])){
  # run time
  eta <- amb[a,]
  filas = c(seq(from=(1+counti*25), to=((1+counti*25)+24)))
  aux_0 <- as.data.frame(read.csv(paste('Tesis_NewModel_NewModel_161123_35_20.csv', sep="")))
  aux <- as.data.frame(aux_0[filas, c(3,4,10)])
  matrix <- matrix(nrow=5, ncol=5)
  colnames(matrix) <- len_S
  rownames(matrix) <- len_I
  count = 1
  for (s in 1:5){
    for (l in 1:5){
      #matrix[s,l] = aux[count,3]
      if (is.na(aux[count,3]) == FALSE){
        matrix[s,l] = aux[count,3]
      }
      else{
        matrix[s,l] = 0
      }
      count = count + 1
    }
  }
  pdf(paste("Timeval_161123_",eta[1],"_",eta[2],".pdf", sep=""))
  plot(matrix[1:5], pch=15, col=1, cex=1.5, ylim=c(0, 5000),
       xlab="demand points", ylab="objective value", xaxt = "n",
       main=paste("Runtime for 16 potential sites \n considering",eta[1],
                  "BLS and",eta[2],"ALS ambulances", sep=" "))
  axis(1, at=1:5, labels=len_I)
  lines(matrix[1:5], lwd=3, col=1)
  points(matrix[6:10], pch=16, cex=1.5, col=2)
  lines(matrix[6:10], lwd=3, col=2)
  points(matrix[11:15], pch=17, cex=1.5, col=3)
  lines(matrix[11:15], lwd=3, col=3)
  points(matrix[16:20], pch=18, cex=1.5, col=4)
  lines(matrix[16:20], lwd=3, col=4)
  points(matrix[21:25], pch=19, cex=1.5, col=6)
  lines(matrix[21:25], lwd=3, col=6)
  legend(x="topleft", legend = len_S, horiz=TRUE, cex = 0.9, fill = c(1, 2, 3, 4, 6), title = "Scenarios")
  dev.off()
  counti = counti+1
}
#}


accidents_covered_total <- data.frame()
for (a in 1:length(amb[,1])){
  eta = amb[a,]
  accidents_covered <- data.frame()
  for (i in len_I){
    for (l in len_L){
      for (s in len_S){

        print(paste('I_Accidents_NewModel_161123_', i,'_',l,'_',s,eta[1],'_',eta[2],'.txt'))

        accident_aux <- as.data.frame(read.table(paste('I_Accidents_NewModel_161123_', i,'_',l,'_',s,'.txt', sep="")))
        accidents <- as.data.frame(read.table(paste('Accidents_NewModel_161123_', i,'_',l,'_',s,'.txt', sep="")))


        aux_0 <- as.data.frame(read.table(paste('OnTime_Obj_NewModel_161123_',i,'_',l,'_',s,'_',eta[1],'_',eta[2],'.txt', sep="")))
        aux_0 <- aux_0[,-2]
        colnames(aux_0) <- c("S", "L", "K", "I", "OnTime")


        aux_1 <- as.data.frame(read.table(paste('Delayed_Obj_NewModel_161123_',i,'_',l,'_',s,'_',eta[1],'_',eta[2],'.txt', sep="")))
        aux_1 <- aux_1[,-2]
        colnames(aux_1) <- c("S", "L", "K", "I", "Delayed")


        aux_2 <- as.data.frame(read.table(paste('NotAssigned_Obj_NewModel_161123_',i,'_',l,'_',s,'_',eta[1],'_',eta[2],'.txt', sep="")))
        aux_2 <- aux_2[,-2]
        colnames(aux_2) <- c("S", "L", "K", "I", "NotAssigned")


        full_expected <- matrix(ncol=s, nrow=1)
        partial1_expected <- matrix(ncol=s, nrow=1)
        partial2_expected <- matrix(ncol=s, nrow=1)
        partial3_expected <- matrix(ncol=s, nrow=1)
        null_expected <- matrix(ncol=s, nrow=1)

        datos <- c()
        datos <- cbind(datos, i, l, s)

        for (s_aux in 1:s){

          demand_points <- matrix(nrow=i, ncol=4)

          if (length(aux_0) != 0){
            on_time <- subset(aux_0, S==s_aux)
          } else{
            on_time <- c(0, 0, 0, 0, 0)
            colnames(on_time) <- c("S", "L", "K", "I", "OnTime")
          }

          if (length(aux_1) != 0){
            delayed <- subset(aux_1, S==s_aux)
          } else{
            delayed <- c(0, 0, 0, 0, 0)
            colnames(delayed) <- c("S", "L", "K", "I", "Delayed")
          }

          if (length(aux_2) != 0){
            notAssigned <- subset(aux_2, S==s_aux)
          } else{
            notAssigned <- c(0, 0, 0, 0, 0)
            colnames(notAssigned) <- c("S", "L", "K", "I", "NotAssigned")
          }

          for (i_aux in 1:i){

            if (accident_aux[s_aux,i_aux] != 0){
              on_time_1 <- subset(on_time, I==i_aux)
              if (length(on_time_1) > 0){
                demand_points[i_aux,1] = length(on_time_1[,1])
              }


              delayed_1 <- subset(delayed, I==i_aux)
              if (length(delayed_1) > 0){
                demand_points[i_aux,2] = length(delayed_1[,1])
              }


              notAssigned_1 <- subset(notAssigned, I==i_aux)
              if (length(notAssigned_1) > 0){
                demand_points[i_aux,3] = sum(notAssigned_1[,5])
              }

            } else{
              demand_points[i_aux,1] = 0
              demand_points[i_aux,2] = 0
              demand_points[i_aux,3] = 0
            }
            demand_points[i_aux,4] = accident_aux[s_aux,i_aux]

          }


          total_full = 0
          total_partial1 = 0
          total_partial2 = 0
          total_partial3 = 0
          total_null = 0
          for (i in 1:i){
            #print(paste("i", i))
            if (demand_points[i,4] != 0){
              if (demand_points[i,3] == demand_points[i,4]){
                total_null = total_null + 1
                #print("null")
              }
              if (demand_points[i,1] == demand_points[i,4]){
                total_full = total_full + 1
                #print("full")
              }
              if (demand_points[i,2] != 0){
                if (demand_points[i,1] + demand_points[i,2] == demand_points[i,4]){
                  total_partial1 = total_partial1 + 1
                  #print("p1")
                }
              }
              if (demand_points[i,3] != 0){
                if(demand_points[i,1] != 0 && demand_points[i,1] + demand_points[i,3] == demand_points[i,4]){
                  total_partial2 = total_partial2 + 1
                  #print("p2")
                }
                if (demand_points[i,2] != 0){
                  if(demand_points[i,1] + demand_points[i,2] + demand_points[i,3] == demand_points[i,4]){
                    total_partial3 = total_partial3 + 1
                    #print("p3")
                  }
                }
              }
            }
          }
          full_expected_s = total_full/as.integer(accidents[s_aux])
          full_expected[1, s_aux] = full_expected_s
          partial1_expected_s = total_partial1/as.integer(accidents[s_aux])
          partial1_expected[1, s_aux] = partial1_expected_s
          partial2_expected_s = total_partial2/as.integer(accidents[s_aux])
          partial2_expected[1, s_aux] = partial2_expected_s
          partial3_expected_s = total_partial3/as.integer(accidents[s_aux])
          partial3_expected[1, s_aux] = partial3_expected_s
          null_expected_s = total_null/as.integer(accidents[s_aux])
          null_expected[1, s_aux] = null_expected_s

        }
        datos <- cbind(datos, prom_full_expected = mean(full_expected)*100)
        datos <- cbind(datos, prom_partial1_expected = mean(partial1_expected)*100)
        datos <- cbind(datos, prom_partial2_expected = mean(partial2_expected)*100)
        datos <- cbind(datos, prom_partial3_expected = mean(partial3_expected)*100)
        datos <- cbind(datos, prom_null_expected = mean(null_expected)*100)
        datos <- cbind(datos, c(eta[1], eta[2]))
        accidents_covered <- rbind(accidents_covered, datos)
      }
    }
  }
  colnames(accidents_covered) <- c("I", "L", "S", "% Full accident coverage", "% Partial1 accident coverage", "% Partial2 accident coverage", "% Partial3 accident coverage", "% Null accident coverage")
  write.csv(accidents_covered, file = paste('ExpectedCoverage_Obj_NewModel_161123_', eta[1],'_',eta[2],'.csv', sep=""), col.names=TRUE, row.names=FALSE, dec = ".")
  aux <- cbind(accidents_covered, eta[1], eta[2])
  colnames(aux) <- c("I", "L", "S", "% Full accident coverage", "% Partial1 accident coverage", "% Partial2 accident coverage", "% Partial3 accident coverage", "% Null accident coverage", "BLS ambulances", "ALS ambulances")
  accidents_covered_total <- rbind(accidents_covered_total, aux)
}
write.csv(accidents_covered_total, file = paste('ExpectedCoverageTotal_Obj_NewModel_161123_','.csv', sep=""), col.names=TRUE, row.names=FALSE, dec = ".")

ind_1 = 1
ind_2 = 5
prom_coverage <- data.frame()
for (a in 1:length(amb[,1])){
  eta = amb[a,]
  for (i in 1:length(len_I)){
    datos <- c()
    datos <- cbind(datos, len_I[i], 16, eta[1], eta[2])
    datos <- cbind(datos, mean(accidents_covered_total[ind_1:ind_2,4]))
    datos <- cbind(datos, mean(accidents_covered_total[ind_1:ind_2,5]))
    datos <- cbind(datos, mean(accidents_covered_total[ind_1:ind_2,6]))
    datos <- cbind(datos, mean(accidents_covered_total[ind_1:ind_2,7]))
    datos <- cbind(datos, mean(accidents_covered_total[ind_1:ind_2,8]))
    
    prom_coverage <- rbind(prom_coverage, datos)
    
    ind_1 = ind_1 + 5
    ind_2 = ind_2 + 5
  }
}
colnames(prom_coverage) <- c("I", "L", "Amb 1", "Amb 2", "Mean % Full", "Mean % P1", "Mean % P2", "Mean % P3", "Mean % Null")
write.csv(prom_coverage, file = paste('MeanCoverageTotal_Obj_NewModel_161123_','.csv', sep=""), col.names=TRUE, row.names=FALSE, dec = ".")


for (a in 1:length(amb[,1])){
  eta = amb[a,]
  pdf(paste("Coverage_161123_",eta[1],"_",eta[2],".pdf", sep=""))
  plot(as.numeric(prom_coverage[a*5-4, 5:9]), pch=15, col=1, cex=1.5,
       ylim=c(0, 100), ylab="% accidents coverage", xlab = "Coverage type", xaxt = "n",
       main=paste("Mean coverage percentage for 16 potential sites \n considering",eta[1],
                  "BLS and",eta[2],"ALS ambulances", sep=" "))
  
  axis(1, at=1:5, labels=c("Full", "Partial1", "Partial2", "Partial3", "Null"))
  lines(as.integer(prom_coverage[a*5-4, 5:9]), lwd=3, col=1)
  points(as.integer(prom_coverage[a*5-3, 5:9]), pch=16, cex=1.5, col=2)
  lines(as.integer(prom_coverage[a*5-3, 5:9]), lwd=3, col=2)
  points(as.integer(prom_coverage[a*5-2, 5:9]), pch=17, cex=1.5, col=3)
  lines(as.integer(prom_coverage[a*5-2, 5:9]), lwd=3, col=3)
  points(as.integer(prom_coverage[a*5-1, 5:9]), pch=18, cex=1.5, col=4)
  lines(as.integer(prom_coverage[a*5-1, 5:9]), lwd=3, col=4)
  points(as.integer(prom_coverage[a*5, 5:9]), pch=19, cex=1.5, col=6)
  lines(as.integer(prom_coverage[a*5, 5:9]), lwd=3, col=6)
  legend(x="topleft", legend = len_I, cex=0.75, fill = c(1, 2, 3, 4, 6),
         title = "Demand points", bty="n")
  dev.off()
}
