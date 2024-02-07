# datos COMPLETOS
amb <- rbind(c(10, 6), c(20, 11), c(35,20))
#amb <- rbind(c(10,6))
# len_I <- c(168, 270, 500, 900, 1500)
# len_L <- c(16, 30, 50, 70, 100)
# len_S <- c(10, 50, 100, 150, 200)

len_I <- c(168, 270, 500, 900, 1500)
len_L <- c(16)
len_S <- c(10, 50, 100, 150, 200)

for (i in len_I){
  for (s in len_S){
    rli_prom_data <- data.frame()
    for (a in 1:length(amb[,1])){
      eta <- amb[a,]
      # first model
      dispatched <- as.data.frame(read.table(paste("Dispatch_ObjZs_Scenarios_060224_", i,"_", len_L[1],"_", s, "_", eta[1], "_", eta[2],".txt", sep="")))
      newdispatched <- subset(dispatched, dispatched[,6] == 1)
      
      # second model
      delayed <- as.data.frame(read.table(paste("Delayed_Obj_NewModel_Supuesto_060224_", i,"_", len_L[1],"_", s, "_", eta[1], "_", eta[2],".txt", sep="")))
      onTime <- as.data.frame(read.table(paste("OnTime_Obj_NewModel_Supuesto_060224_", i,"_", len_L[1],"_", s, "_", eta[1], "_", eta[2],".txt", sep="")))
      
      #both models
      accidents_scenarios <- as.data.frame(read.table(paste("ScAccidents_ObjZs_Scenarios_060224_", i,"_", len_L[1],"_", s,".txt", sep="")))
      cli <- as.data.frame(read.table(paste("Cli_ObjZs_Scenarios_060224_", i,"_", len_L[1],"_", s,".txt", sep="")))
      rli <- as.data.frame(read.table(paste("rli_ObjZs_Scenarios_060224_", i,"_", len_L[1],"_", s,".txt", sep="")))
      
      
      for (s_ind in 1:s){
        for (i_ind in 1:i){
          
          # si hay accidentes para k = 1
          if (accidents_scenarios[s_ind, (i_ind*2)-1] != 0){
            # first model
            model1_sub <- subset(newdispatched, newdispatched[,2] == s_ind)
            model1_sub1 <- subset(model1_sub, model1_sub[,5] == i_ind)
            model1_sub2 <- subset(model1_sub1, model1_sub1[,4] == 1)
            minutos1 = 0
            if (length(model1_sub2[,1]) > 0){
              for (m1 in 1:length(model1_sub2[,1])){
                ind_l = model1_sub2[m1,3]
                ind_i = model1_sub2[m1,5]
                minutos1 = minutos1 + as.numeric(rli[ind_l,ind_i])
              }
              rli_model1_prom1 <- minutos1/length(model1_sub2[,1])
            }else{
              rli_model1_prom1 = 0
            }
            
            #second model
            model2_sub <- subset(onTime, onTime[,1] == s_ind)
            model2_sub1 <- subset(model2_sub, model2_sub[,5] == i_ind)
            model2_sub2 <- subset(model2_sub1, model2_sub1[,4] == 1)
            
            model2_sub_2 <- subset(delayed, delayed[,1] == s_ind)
            model2_sub1_2 <- subset(model2_sub_2, model2_sub_2[,5] == i_ind)
            model2_sub2_2 <- subset(model2_sub1_2, model2_sub1_2[,4] == 1)
            
            minutos2 = 0
            if (length(model2_sub2[,1]) > 0 || length(model2_sub2_2[,1]) > 0){
              if (length(model2_sub2[,1]) > 0){
                for (m2 in 1:length(model2_sub2[,1])){
                  ind_l = model2_sub2[m2,3]
                  ind_i = model2_sub2[m2,5]
                  minutos2 = minutos2 + as.numeric(rli[ind_l,ind_i])
                }
              }
              
              if (length(model2_sub2_2[,1]) > 0){
                for (m3 in 1:length(model2_sub2_2[,1])){
                  ind_l = model2_sub2_2[m3,3]
                  ind_i = model2_sub2_2[m3,5]
                  minutos2 = minutos2 + as.numeric(rli[ind_l,ind_i])
                }
              }
              rli_model2_prom1 <- minutos2/(length(model2_sub2[,1])+length(model2_sub2_2[,1]))
              
            }else{
              rli_model2_prom1 = 0
            }
            
          }else{
            rli_model1_prom1 = 0
            rli_model2_prom1 = 0
          }
          
          # si hay accidentes para k = 2
          if (accidents_scenarios[s_ind, i_ind*2] != 0){
            # first model
            model1_sub <- subset(newdispatched, newdispatched[,2] == s_ind)
            model1_sub1 <- subset(model1_sub, model1_sub[,5] == i_ind)
            model1_sub2 <- subset(model1_sub1, model1_sub1[,4] == 2)
            minutos1 = 0
            if (length(model1_sub2[,1]) > 0){
              for (m1 in 1:length(model1_sub2[,1])){
                ind_l = model1_sub2[m1,3]
                ind_i = model1_sub2[m1,5]
                minutos1 = minutos1 + as.numeric(rli[ind_l,ind_i])
              }
              rli_model1_prom2 <- minutos1/length(model1_sub2[,1])
            }else{
              rli_model1_prom2 = 0
            }
            
            
            #second model
            model2_sub <- subset(onTime, onTime[,1] == s_ind)
            model2_sub1 <- subset(model2_sub, model2_sub[,5] == i_ind)
            model2_sub2 <- subset(model2_sub1, model2_sub1[,4] == 2)
            
            model2_sub_2 <- subset(delayed, delayed[,1] == s_ind)
            model2_sub1_2 <- subset(model2_sub_2, model2_sub_2[,5] == i_ind)
            model2_sub2_2 <- subset(model2_sub1_2, model2_sub1_2[,4] == 2)
            
            minutos2 = 0
            if (length(model2_sub2[,1]) > 0 || length(model2_sub2_2[,1]) > 0){
              if (length(model2_sub2[,1]) > 0){
                for (m2 in 1:length(model2_sub2[,1])){
                  ind_l = model2_sub2[m2,3]
                  ind_i = model2_sub2[m2,5]
                  minutos2 = minutos2 + as.numeric(rli[ind_l,ind_i])
                }
              }
            
              if (length(model2_sub2_2[,1]) > 0){
                for (m3 in 1:length(model2_sub2_2[,1])){
                  ind_l = model2_sub2_2[m3,3]
                  ind_i = model2_sub2_2[m3,5]
                  minutos2 = minutos2 + as.numeric(rli[ind_l,ind_i])
                }
              }
              
              rli_model2_prom2 <- minutos2/(length(model2_sub2[,1])+length(model2_sub2_2[,1]))
              
            }else{
              rli_model2_prom1 = 0
            }
          }else{
            rli_model1_prom2 = 0
            rli_model2_prom2 = 0
          }
          
          if (accidents_scenarios[s_ind, (i_ind*2)-1] != 0 || accidents_scenarios[s_ind, i_ind*2] != 0){
            rli_prom_data <- rbind(rli_prom_data, c(s_ind, i_ind, rli_model1_prom1, rli_model2_prom1, rli_model1_prom2, rli_model2_prom2))
          }
        }
      }
      
    }
    colnames(rli_prom_data) <- c("S","I","M1 k1","M2 k1","M1 k2", "M2 k2")
    write.csv(rli_prom_data, file = paste('mean_rli_bothModels_',i,"_",len_L[1],"_",s,"_AllAmb",'.csv', sep=""), col.names=TRUE, row.names=FALSE, dec = ".")
  }
}
