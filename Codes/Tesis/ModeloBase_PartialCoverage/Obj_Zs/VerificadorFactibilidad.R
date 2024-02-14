# datos COMPLETOS
amb <- rbind(c(10, 6), c(20, 11), c(35,20))
#amb <- rbind(c(10,6))
# len_I <- c(168, 270, 500, 900, 1500)
# len_L <- c(16, 30, 50, 70, 100)
# len_S <- c(10, 50, 100, 150, 200)

len_I <- c(168, 270, 500, 900, 1500)
len_L <- c(16)
len_S <- c(10, 50, 100, 150, 200)

factibilidad <- data.frame()
for (i in len_I){
  for (l in len_L){
    for (s in len_S){
      rli_prom_data <- data.frame()
      for (a in 1:length(amb[,1])){
        eta <- amb[a,]
        
        # First_Model_ObjZs
        instance <- c()
        instance <- cbind(instance, "M1Supuesto", i, l, s, eta[1], eta[2])
        
        # Verificar si se localizaron <= ambulancias disponibles en el sistema
        k1_located = 0
        k2_located = 0
        located <- delayed <- as.data.frame(read.table(paste("Location_ObjZs_Scenarios_060224_", i,"_", len_L[1],"_", s, "_", eta[1], "_", eta[2],".txt", sep="")))
        for (locate in 1:length(located[,1])){
          if(located[locate,3] == 1){
            k1_located = k1_located + located[locate,4]
          }
          if(located[locate,3] == 2){
            k2_located = k2_located + located[locate,4]
          }
        }
        if (k1_located <= eta[1]){
          instance <- cbind(instance, "Yes")
        } else{
          instance <- cbind(instance, "No")
        }
        
        if (k2_located <= eta[2]){
          instance <- cbind(instance, "Yes")
        } else{
          instance <- cbind(instance, "No")
        }
        
        # Verificar si se despacharon <= de las localizadas
        dispatch <- as.data.frame(read.table(paste("Dispatch_ObjZs_Scenarios_060224_", i,"_", len_L[1],"_", s, "_", eta[1], "_", eta[2],".txt", sep="")))
        new_dispatch <- subset(dispatch, dispatch[,6] == 1)
        
        k1_del_fact <- c()
        k2_del_fact <- c()
        k1_ont_fact <- c()
        k2_ont_fact <- c()
        k1_disp_fact <- c()
        k2_disp_fact <- c()
        
        for (sce in 1:s){
          
          k1_delayed = -1
          k2_delayed = -1
          k1_onTime = -1
          k2_onTime = -1
          k1_dispatched = 0
          k2_dispatched = 0
          
          # delayed
          new_dispatch_aux <- subset(new_dispatch, new_dispatch[,2] == sce)
          if (length(new_dispatch_aux[,1]) > 0){
            for (len in 1:length(new_dispatch_aux[,1])){
              if(new_dispatch_aux[len,4] == 1){
                k1_dispatched = k1_dispatched + 1
              }
              if(new_dispatch_aux[len,4] == 2){
                k2_dispatched = k2_dispatched + 1
              }
            }
          } else{
            k1_dispatched = 0
            k2_dispatched = 0
          }
          
          if (k1_delayed <= k1_located){
            k1_del_fact <- cbind(k1_del_fact, "Yes")
          } else{
            k1_del_fact <- cbind(k1_del_fact, "No")
          }
          
          if (k2_delayed <= k2_located){
            k2_del_fact <- cbind(k2_del_fact, "Yes")
          } else{
            k2_del_fact <- cbind(k2_del_fact, "No")
          }
          
          if (k1_onTime <= k1_located){
            k1_ont_fact <- cbind(k1_ont_fact, "Yes")
          } else{
            k1_ont_fact <- cbind(k1_ont_fact, "No")
          }
          
          if (k2_onTime <= k2_located){
            k2_ont_fact <- cbind(k2_ont_fact, "Yes")
          } else{
            k2_ont_fact <- cbind(k2_ont_fact, "No")
          }
          
          # total dispatched
          if (k1_dispatched <= k1_located){
            k1_disp_fact <- cbind(k1_disp_fact, "Yes")
          } else{
            k1_disp_fact <- cbind(k1_disp_fact, "No")
          }
          if (k2_dispatched <= k2_located){
            k2_disp_fact <- cbind(k2_disp_fact, "Yes")
          } else{
            k2_disp_fact <- cbind(k2_disp_fact, "No")
          }
          
        }
        
        # delayed 
        if (all(k1_del_fact == "Yes") == "TRUE"){
          instance <- cbind(instance, "Yes")
        } else{
          instance <- cbind(instance, "No")
        }
        
        if (all(k2_del_fact == "Yes") == "TRUE"){
          instance <- cbind(instance, "Yes")
        } else{
          instance <- cbind(instance, "No")
        }
        
        # onTime
        if (all(k1_ont_fact == "Yes") == "TRUE"){
          instance <- cbind(instance, "Yes")
        } else{
          instance <- cbind(instance, "No")
        }
        
        if (all(k2_ont_fact == "Yes") == "TRUE"){
          instance <- cbind(instance, "Yes")
        } else{
          instance <- cbind(instance, "No")
        }
        
        # total dispatched
        if (all(k1_disp_fact == "Yes") == "TRUE"){
          instance <- cbind(instance, "Yes")
        } else{
          instance <- cbind(instance, "No")
        }
        
        if (all(k2_disp_fact == "Yes") == "TRUE"){
          instance <- cbind(instance, "Yes")
        } else{
          instance <- cbind(instance, "No")
        }
        
        factibilidad <- rbind(factibilidad, instance) 
        
        # NewModel_Supuesto
        instance <- c()
        instance <- cbind(instance, "M2Supuesto", i, l, s, eta[1], eta[2])

        # Verificar si se localizaron <= ambulancias disponibles en el sistema
        k1_located = 0
        k2_located = 0
        located <- delayed <- as.data.frame(read.table(paste("Location_Obj_NewModel_Supuesto_060224_", i,"_", len_L[1],"_", s, "_", eta[1], "_", eta[2],".txt", sep="")))
        for (locate in 1:length(located[,1])){
          if(located[locate,2] == 1){
            k1_located = k1_located + located[locate,3]
          }
          if(located[locate,2] == 2){
            k2_located = k2_located + located[locate,3]
          }
        }
        if (k1_located <= eta[1]){
          instance <- cbind(instance, "Yes")
        } else{
          instance <- cbind(instance, "No")
        }

        if (k2_located <= eta[2]){
          instance <- cbind(instance, "Yes")
        } else{
          instance <- cbind(instance, "No")
        }

        # Verificar si se despacharon <= de las localizadas
        delayed <- as.data.frame(read.table(paste("Delayed_Obj_NewModel_Supuesto_060224_", i,"_", len_L[1],"_", s, "_", eta[1], "_", eta[2],".txt", sep="")))
        onTime <- as.data.frame(read.table(paste("OnTime_Obj_NewModel_Supuesto_060224_", i,"_", len_L[1],"_", s, "_", eta[1], "_", eta[2],".txt", sep="")))

        k1_del_fact <- c()
        k2_del_fact <- c()
        k1_ont_fact <- c()
        k2_ont_fact <- c()
        k1_disp_fact <- c()
        k2_disp_fact <- c()

        for (sce in 1:s){

          k1_delayed = 0
          k1_onTime = 0
          k2_delayed = 0
          k2_onTime = 0

          k1_dispatched = 0
          k2_dispatched = 0

          # delayed
          delayed_aux <- subset(delayed, delayed[,1] == sce)
          if (length(delayed_aux[,1]) > 0){
            for (len in 1:length(delayed_aux[,1])){
              if(delayed_aux[len,4] == 1){
                k1_delayed = k1_delayed + 1
                k1_dispatched = k1_dispatched + 1
              }
              if(delayed_aux[len,4] == 2){
                k2_delayed = k2_delayed + 1
                k2_dispatched = k2_dispatched + 1
              }
            }
          } else{
            k1_delayed = 0
            k2_delayed = 0
          }

          if (k1_delayed <= k1_located){
            k1_del_fact <- cbind(k1_del_fact, "Yes")
          } else{
            k1_del_fact <- cbind(k1_del_fact, "No")
          }

          if (k2_delayed <= k2_located){
            k2_del_fact <- cbind(k2_del_fact, "Yes")
          } else{
            k2_del_fact <- cbind(k2_del_fact, "No")
          }

          # on time
          onTime_aux <- subset(onTime, onTime[,1] == sce)
          if (length(onTime_aux[,1]) > 0){
            for (len in 1:length(onTime_aux[,1])){
              if(onTime_aux[len,4] == 1){
                k1_onTime = k1_onTime + 1
                k1_dispatched = k1_dispatched + 1
              }
              if(onTime_aux[len,4] == 2){
                k2_onTime = k2_onTime + 1
                k2_dispatched = k2_dispatched + 1
              }
            }
          } else{
            k1_onTime = 0
            k2_onTime = 0
          }

          if (k1_onTime <= k1_located){
            k1_ont_fact <- cbind(k1_ont_fact, "Yes")
          } else{
            k1_ont_fact <- cbind(k1_ont_fact, "No")
          }

          if (k2_onTime <= k2_located){
            k2_ont_fact <- cbind(k2_ont_fact, "Yes")
          } else{
            k2_ont_fact <- cbind(k2_ont_fact, "No")
          }

          # total dispatched
          if (k1_dispatched <= k1_located){
            k1_disp_fact <- cbind(k1_disp_fact, "Yes")
          } else{
            k1_disp_fact <- cbind(k1_disp_fact, "No")
          }
          if (k2_dispatched <= k2_located){
            k2_disp_fact <- cbind(k2_disp_fact, "Yes")
          } else{
            k2_disp_fact <- cbind(k2_disp_fact, "No")
          }

        }

        # delayed
        if (all(k1_del_fact == "Yes") == "TRUE"){
          instance <- cbind(instance, "Yes")
        } else{
          instance <- cbind(instance, "No")
        }

        if (all(k2_del_fact == "Yes") == "TRUE"){
          instance <- cbind(instance, "Yes")
        } else{
          instance <- cbind(instance, "No")
        }

        # onTime
        if (all(k1_ont_fact == "Yes") == "TRUE"){
          instance <- cbind(instance, "Yes")
        } else{
          instance <- cbind(instance, "No")
        }

        if (all(k2_ont_fact == "Yes") == "TRUE"){
          instance <- cbind(instance, "Yes")
        } else{
          instance <- cbind(instance, "No")
        }

        # total dispatched
        if (all(k1_disp_fact == "Yes") == "TRUE"){
          instance <- cbind(instance, "Yes")
        } else{
          instance <- cbind(instance, "No")
        }

        if (all(k2_disp_fact == "Yes") == "TRUE"){
          instance <- cbind(instance, "Yes")
        } else{
          instance <- cbind(instance, "No")
        }

        factibilidad <- rbind(factibilidad, instance)

        
        
        # NewModel_NewModel_SinDiferenciaEnK
        instance <- c()
        instance <- cbind(instance, "M2SinSupuesto", i, l, s, eta[1], eta[2])

        # Verificar si se localizaron <= ambulancias disponibles en el sistema
        k1_located = 0
        k2_located = 0
        located <- delayed <- as.data.frame(read.table(paste("Location_Obj_NewModel_NewModel_060224_", i,"_", len_L[1],"_", s, "_", eta[1], "_", eta[2],".txt", sep="")))
        for (locate in 1:length(located[,1])){
          if(located[locate,2] == 1){
            k1_located = k1_located + located[locate,3]
          }
          if(located[locate,2] == 2){
            k2_located = k2_located + located[locate,3]
          }
        }
        if (k1_located <= eta[1]){
          instance <- cbind(instance, "Yes")
        } else{
          instance <- cbind(instance, "No")
        }

        if (k2_located <= eta[2]){
          instance <- cbind(instance, "Yes")
        } else{
          instance <- cbind(instance, "No")
        }

        # Verificar si se despacharon <= de las localizadas
        delayed <- as.data.frame(read.table(paste("Delayed_Obj_NewModel_NewModel_060224_", i,"_", len_L[1],"_", s, "_", eta[1], "_", eta[2],".txt", sep="")))
        onTime <- as.data.frame(read.table(paste("OnTime_Obj_NewModel_NewModel_060224_", i,"_", len_L[1],"_", s, "_", eta[1], "_", eta[2],".txt", sep="")))

        k1_del_fact <- c()
        k2_del_fact <- c()
        k1_ont_fact <- c()
        k2_ont_fact <- c()
        k1_disp_fact <- c()
        k2_disp_fact <- c()

        for (sce in 1:s){

          k1_delayed = 0
          k1_onTime = 0
          k2_delayed = 0
          k2_onTime = 0

          k1_dispatched = 0
          k2_dispatched = 0

          # delayed
          delayed_aux <- subset(delayed, delayed[,1] == sce)
          if (length(delayed_aux[,1]) > 0){
            for (len in 1:length(delayed_aux[,1])){
              if(delayed_aux[len,4] == 1){
                k1_delayed = k1_delayed + 1
                k1_dispatched = k1_dispatched + 1
              }
              if(delayed_aux[len,4] == 2){
                k2_delayed = k2_delayed + 1
                k2_dispatched = k2_dispatched + 1
              }
            }
          } else{
            k1_delayed = 0
            k2_delayed = 0
          }

          if (k1_delayed <= k1_located){
            k1_del_fact <- cbind(k1_del_fact, "Yes")
          } else{
            k1_del_fact <- cbind(k1_del_fact, "No")
          }

          if (k2_delayed <= k2_located){
            k2_del_fact <- cbind(k2_del_fact, "Yes")
          } else{
            k2_del_fact <- cbind(k2_del_fact, "No")
          }

          # on time
          onTime_aux <- subset(onTime, onTime[,1] == sce)
          if (length(onTime_aux[,1]) > 0){
            for (len in 1:length(onTime_aux[,1])){
              if(onTime_aux[len,4] == 1){
                k1_onTime = k1_onTime + 1
                k1_dispatched = k1_dispatched + 1
              }
              if(onTime_aux[len,4] == 2){
                k2_onTime = k2_onTime + 1
                k2_dispatched = k2_dispatched + 1
              }
            }
          } else{
            k1_onTime = 0
            k2_onTime = 0
          }

          if (k1_onTime <= k1_located){
            k1_ont_fact <- cbind(k1_ont_fact, "Yes")
          } else{
            k1_ont_fact <- cbind(k1_ont_fact, "No")
          }

          if (k2_onTime <= k2_located){
            k2_ont_fact <- cbind(k2_ont_fact, "Yes")
          } else{
            k2_ont_fact <- cbind(k2_ont_fact, "No")
          }

          # total dispatched
          if (k1_dispatched <= k1_located){
            k1_disp_fact <- cbind(k1_disp_fact, "Yes")
          } else{
            k1_disp_fact <- cbind(k1_disp_fact, "No")
          }
          if (k2_dispatched <= k2_located){
            k2_disp_fact <- cbind(k2_disp_fact, "Yes")
          } else{
            k2_disp_fact <- cbind(k2_disp_fact, "No")
          }

        }

        # delayed
        if (all(k1_del_fact == "Yes") == "TRUE"){
          instance <- cbind(instance, "Yes")
        } else{
          instance <- cbind(instance, "No")
        }

        if (all(k2_del_fact == "Yes") == "TRUE"){
          instance <- cbind(instance, "Yes")
        } else{
          instance <- cbind(instance, "No")
        }

        # onTime
        if (all(k1_ont_fact == "Yes") == "TRUE"){
          instance <- cbind(instance, "Yes")
        } else{
          instance <- cbind(instance, "No")
        }

        if (all(k2_ont_fact == "Yes") == "TRUE"){
          instance <- cbind(instance, "Yes")
        } else{
          instance <- cbind(instance, "No")
        }

        # total dispatched
        if (all(k1_disp_fact == "Yes") == "TRUE"){
          instance <- cbind(instance, "Yes")
        } else{
          instance <- cbind(instance, "No")
        }

        if (all(k2_disp_fact == "Yes") == "TRUE"){
          instance <- cbind(instance, "Yes")
        } else{
          instance <- cbind(instance, "No")
        }

        factibilidad <- rbind(factibilidad, instance)
      }
    }
  }
}
colnames(factibilidad) <- c("Model", "I", "L", "S", "|K1|", "|K2|", "Locate_K1", "Locate_K2", "Delay_K1", "Delay_K2", "OnTime_K1", "OnTime_K2", "Dispatched_K1", "Dispatched_K2")
write.csv(factibilidad, file = paste('feasibility_AllInstances_AllAmb_060224','.csv', sep=""), col.names=TRUE, row.names=FALSE, dec = ".")