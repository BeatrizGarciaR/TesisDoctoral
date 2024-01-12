# datos COMPLETOS
#amb <- rbind(c(10, 6), c(20, 11), c(35,20))
amb <- rbind(c(10,6))
# len_I <- c(168, 270, 500, 900, 1500)
# len_L <- c(16, 30, 50, 70, 100)
# len_S <- c(10, 50, 100, 150, 200)

len_I <- c(168)
len_L <- c(16)
len_S <- c(10)

for (a in 1:length(amb[,1])){
  eta <- amb[a,]
  for (i in len_I){
    for (s in len_S){
      
      # first model
      dispatched <- as.data.frame(read.table(paste("Dispatch_ObjZs_Scenarios_161123_", i,"_", len_L[1],"_", s, "_", eta[1], "_", eta[2],".txt", sep="")))
      newdispatched <- subset(dispatched, dispatched[,6] == 1)
      
      # second model
      delayed <- as.data.frame(read.table(paste("Delayed_Obj_NewModel_010124_", i,"_", len_L[1],"_", s, "_", eta[1], "_", eta[2],".txt", sep="")))
      onTime <- as.data.frame(read.table(paste("OnTime_Obj_NewModel_010124_", i,"_", len_L[1],"_", s, "_", eta[1], "_", eta[2],".txt", sep="")))
      
      #both models
      accidents_scenarios <- as.data.frame(read.table(paste("ScAccidents_ObjZs_Scenarios_161123_", i,"_", len_L[1],"_", s,".txt", sep="")))
      cli <- as.data.frame(read.table(paste("Cli_ObjZs_Scenarios_161123_", i,"_", len_L[1],"_", s,".txt", sep="")))
      rli <- as.data.frame(read.table(paste("rli_ObjZs_Scenarios_161123_", i,"_", len_L[1],"_", s,".txt", sep="")))
      
      # for (s_ind in 1:s){
      #   for (i_ind in 1:i){
      #     if (accidents_scenarios[s_ind, (i_ind*2)-1] != 0){
      #       model1_subset <- subset(newdispatched, newdispatched[,4] == 1)
      #     }
      #     if (accidents_scenarios[s_ind, i_ind*2] != 0){
      #       
      #     }
      #   }
      # }

    }
  }
}
