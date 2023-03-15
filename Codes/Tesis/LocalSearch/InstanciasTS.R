########################
###### Instancias ######
########################

# tamanos_I <- c(20, 50, 80, 95)
# tamanos_L <- c(40, 50, 70, 85)
# tamanos_S <- c(12, 25, 30, 40)
tamanos_I <- c(1000)
tamanos_L <- c(200)
tamanos_S <- c(500)
porcentaje_L1 = 0.65
t = 9
tmax = 25
K <- c(1, 2)

for (iconj in 1:length(tamanos_I)){
  for (jconj in 1:length(tamanos_L)){
    len_I = tamanos_I[iconj]
    len_L = tamanos_L[jconj]
    I <- c()
    for (i in 1:len_I){
      I <- cbind(I, i)
    }
    
    L <- c()
    for (l in 1:len_L){
      L <- cbind(L, l)
    }
    
    pickL1 = as.integer(tamanos_L[jconj]*porcentaje_L1)
    L1 = sample(1:len_L, pickL1)
    
    # Specify sample size
    N <- len_I  ### Quiero i valores pero en cada potencial l
    
    r_li <- c()
    for (sites in 1:len_L){
      # Draw N gamma distributed values
      y_rgamma <- rgamma(N, shape = 14.2, rate = .85)

      # Print values to RStudio console
      r_li <- rbind(r_li, as.integer(y_rgamma))
    }
    
    # r_li <- c()
    # for (sites in 1:len_L){
    #   # Draw N gamma distributed values
    #   #y_rgamma <- rgamma(N, shape = 14.2, rate = .85) 
    #   y_rgamma <- c()
    #   for(n in 1:N){
    #     y_gamma <- rnorm(1, 20, 6)
    #     # Print values to RStudio console
    #     y_rgamma <- cbind(y_rgamma, as.integer(y_gamma))
    #   }
    #   r_li <- rbind(r_li, y_rgamma) 
    # }
    
    for (sconj in 1:length(tamanos_S)){
      #Nombre: Instancias_Prueba_I_L_S
      
      instancename <- paste('Instancias_Prueba_',toString(tamanos_I[iconj]),'_',
                            toString(tamanos_L[jconj]),'_', toString(tamanos_S[sconj]),'.txt', sep = "")

      ################################
      ############# SETS #############
      ################################
      
      write(len_I, file = instancename)
      
      write(len_L, file = instancename, append=TRUE)
      
      len_S = tamanos_S[sconj]
      write(len_S, file = instancename, append=TRUE)
      
      ################################
      ########## SCENARIOS ###########
      ################################
      
      ###### NORMALIZADO 
      xs <- rexp(len_S*len_I*length(K), rate = 1)
      S <- matrix(nrow=len_S, ncol=len_I*length(K))
      sig <- 0
      for (len in 1:(len_I*length(K))){
        rand = rnorm(1)
        if (rand < 1){
          for (s in 1:len_S){
            S[s, len] = 0
          }
        }
        else{
          for (s in 1:len_S){
            sig <- sig + 1
            if (xs[sig] < 1){
              S[s, len] = 0
            }
            else if (xs[sig] < 2){
              S[s, len] = 1
            }
            else{
              S[s, len] = 2
            }
          }
        }
      }
      
      
      ###### NO NORMALIZADO 
      # xs <- rexp(len_S*len_I*length(K), rate = 2)
      # #xs <- rbinom(len_S*len_I*length(K), 1, 0.5)
      # S <- matrix(nrow=len_S, ncol=len_I*length(K))
      # sig <- 0
      # for (s in 1:len_S){
      #   rand = rnorm(1)
      #   if (rand < 1){
      #     for (len in 1:(len_I*length(K))){
      #       S[s, len] = 0
      #     }
      #   }
      #   else{
      #     for (len in 1:(len_I*length(K))){
      #       #x <- rexp(1, rate = 2)
      #       #if (len < len_I*length(K)/3 || len > len_I*length(K) - len_I*length(K)/3){
      #       randi = rnorm(1)
      #       if (randi < 0.8){
      #         S[s, len] = 0
      #       }
      #       else{
      #         sig = sig + 1
      #         x = xs[sig]
      #         # if (x == 0){
      #         #   S[s, len] = 1
      #         # }
      #         # else{
      #         #   S[s, len] = 2
      #         # }
      #         if (x < 0.5){
      #           S[s, len] = 0
      #         }
      #         else if (x < 2){
      #           S[s, len] = 1
      #         }
      #         else{
      #           S[s, len] = 2
      #         }
      #       }
      # 
      #     }
      #   }
      # }
      
      # S <- c()
      # for (s in 1:len_S){
      #   S <- rbind(S, rbinom(len_I*length(K), 2, 0.1))
      # }
      write.table(S, file = instancename, row.names = FALSE, col.names = FALSE, append=TRUE)
      
      ################################
      ####### RESPONSE TIMES #########
      ################################
      
      write.table(r_li, file = instancename, row.names = FALSE, col.names = FALSE, append=TRUE)
      
      ################################
      ############ C_li ##############
      ################################     
      
      c_li <- c()
      for (l in 1:len_L){
        c_li_aux <- c()
        for (i in 1:len_I){
          if (r_li[l,i] <= t){
            c_li_aux <- cbind(c_li_aux, 1)
          }
          else {
            if (t < r_li[l,i] &&  r_li[l,i] < tmax){
              d_rli = 1 - ((r_li[l,i]-t)/(tmax-t))
              c_li_aux <- cbind(c_li_aux, d_rli)
            }
            else{
              c_li_aux <- cbind(c_li_aux, 0)
            }
          }
        }
        c_li <- rbind(c_li, c_li_aux)
      }
      
      write.table(c_li, file = instancename, row.names = FALSE, col.names = FALSE, append=TRUE) 
      
    }
  }
}
  
