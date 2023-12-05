#amb <- rbind(c(10, 6), c(20, 11), c(35,20))
amb <- rbind(c(10,6), c(20,11), c(35,20))
# len_I <- c(168, 270, 500, 900, 1500)
# len_L <- c(16, 30, 50, 70, 100)
# len_S <- c(10, 50, 100, 150, 200)

len_I <- c(168, 270, 500, 900, 1500)
len_L <- c(16)
len_S <- c(10, 50, 100, 150, 200)


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
          on_time <- subset(aux_0, S==s_aux)
          delayed <- subset(aux_1, S==s_aux)
          notAssigned <- subset(aux_2, S==s_aux)
          
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
                if(demand_points[i,1] + demand_points[i,3] == demand_points[i,4]){
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
        accidents_covered <- rbind(accidents_covered, datos)
      }
    }
  }
  colnames(accidents_covered) <- c("I", "L", "S", "% Full accident coverage", "% Partial1 accident coverage", "% Partial2 accident coverage", "% Partial3 accident coverage", "% Null accident coverage")
  write.csv(accidents_covered, file = paste('ExpectedCoverage_ObjZs_Scenarios_161123_', eta[1],'_',eta[2],'.csv', sep=""), col.names=TRUE, row.names=FALSE, dec = ".")
  aux <- cbind(accidents_covered, eta[1], eta[2])
  colnames(aux) <- c("I", "L", "S", "% Full accident coverage", "% Partial1 accident coverage", "% Partial2 accident coverage", "% Partial3 accident coverage", "% Null accident coverage", "BLS ambulances", "ALS ambulances")
  accidents_covered_total <- rbind(accidents_covered_total, aux)
}
write.csv(accidents_covered_total, file = paste('ExpectedCoverageTotal_ObjZs_Scenarios_161123_','.csv', sep=""), col.names=TRUE, row.names=FALSE, dec = ".")
