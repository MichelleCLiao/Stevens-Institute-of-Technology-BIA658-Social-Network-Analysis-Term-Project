library(tidyverse)
library(igraph)
library(ggplot2)
install.packages("xlsx")
library(xlsx)
?as.matrix()
#get the plot
matrix1=read.csv('edge_unweighted.csv',header=T)

a<-matrix1$X0
rownames(matrix1)<-a
matrix1<-subset(matrix1,select =-X0)
colnames(matrix1)<-a
as<-as.matrix(matrix1)

g1 <- graph.adjacency(as, mode = "undirected")
g1<-simplify(g1)
vertex_attr(g1)
edge_attr(g1)

#set the plot's weight
matrix2<-read.csv('edge_similarity.csv')
b<-matrix2$X0
rownames(matrix2)<-b
matrix2<-subset(matrix2,select =-X0)
colnames(matrix2)<-b
matrix2
# get the weight of the plot
g1weight<- as.list(matrix2)
g1weight<-unlist(g1weight)
g1weight<-g1weight[g1weight!=0]
#as2<-as.matrix(matrix2)
#g1<-set_graph_attr(g1,'weight',as2)
#graph_attr(g1,'weight')
E(g1)
E(g1)$weight
E(g1)$weight<-g1weight

#get the region
region<-read.csv('boro_precinct2.csv',header=F)
region <- region[-1,]
head(region)
# make the edge and the node in the same region the same region value
V(g1)$region<-region$V1
for(i in 1:258){
  a = ends(g1, i)[1]
  b = ends(g1, i)[2]
  for (j in V(g1)){
    if(V(g1)[j]$name==a){
      for(k in V(g1)){
        if(V(g1)[k]$name==b){
          E(g1)[i]$region<-V(g1)[j]$region
        } 
      }
    }
  }
}
V(g1)[1]$region

g2<-g1
graph.density(g2)
criminal_rate<-read.csv('crime_per_thousand_people.csv')
head(criminal_rate)
V(g2)$osize<-criminal_rate$crime.thousand_people
par(mar = c(0, 2, 0, 0))
V(g2)$osize


#this is the community, but i think it's useless for this pic
#com = walktrap.community(g2,steps=5,merges = TRUE,
#                         modularity = TRUE, membership = TRUE)
#V(g2)$sg=com$membership

#use community
#calculate teh community
vertex_attr(g2)
edge_attr(g2)
cl <- optimal.community(g2)
V(g2)$community <- cl$membership
#-----------------felony---------------
matrixf=read.csv('level_network/felony_unweighted.csv',header=T)

a<-matrixf$X0
rownames(matrixf)<-a
matrixf<-subset(matrixf,select =-X0)
colnames(matrixf)<-a
as<-as.matrix(matrixf)

gf <- graph.adjacency(as, mode = "undirected")
gf<-simplify(gf)
vertex_attr(gf)
edge_attr(gf)
E(gf)

#set the plot's weight
matrixf2<-read.csv('level_network/felony_similarity.csv')
b<-matrixf2$X0
rownames(matrixf2)<-b
matrixf2<-subset(matrixf2,select =-X0)
colnames(matrixf2)<-b
matrixf2
# get the weight of the plot
g1weight<- as.list(matrixf2)
g1weight<-unlist(g1weight)
g1weight<-g1weight[g1weight!=0]
#as2<-as.matrix(matrix2)
#g1<-set_graph_attr(g1,'weight',as2)
#graph_attr(g1,'weight')
E(gf)
E(gf)$weight
E(gf)$weight<-g1weight
#get the region
region<-read.csv('boro_precinct2.csv',header=F)
region <- region[-1,]
head(region)
# make the edge and the node in the same region the same region value
V(gf)$region<-region$V1
for(i in 1:257){
  a = ends(gf, i)[1]
  b = ends(gf, i)[2]
  for (j in V(gf)){
    if(V(gf)[j]$name==a){
      for(k in V(g1)){
        if(V(gf)[k]$name==b){
          E(gf)[i]$region<-V(gf)[j]$region
        } 
      }
    }
  }
}
V(gf)[1]$region

graph.density(gf)
criminal_rate<-read.csv('level_network/felony_rate.csv')
head(criminal_rate)
V(gf)$osize<-criminal_rate$crime.thousand_people
par(mar = c(0, 2, 0, 0))
V(gf)$osize

#calculate teh community
vertex_attr(gf)
edge_attr(gf)
cl <- optimal.community(gf)
V(gf)$community <- cl$membership

#------------------misdemeanor----------------------------
matrixm=read.csv('level_network/misdemeanor_unweighted.csv',header=T)

a<-matrixm$X0
rownames(matrixm)<-a
matrixm<-subset(matrixm,select =-X0)
colnames(matrixm)<-a
as<-as.matrix(matrixm)

gm <- graph.adjacency(as, mode = "undirected")
gm<-simplify(gm)

matrixm2<-read.csv('level_network/misdemeanor_similarity.csv')
b<-matrixm2$X0
rownames(matrixm2)<-b
matrixm2<-subset(matrixm2,select =-X0)
colnames(matrixm2)<-b

# get the weight of the plot
g1weight<- as.list(matrixm2)
g1weight<-unlist(g1weight)
g1weight<-g1weight[g1weight!=0]

#as2<-as.matrix(matrix2)
#g1<-set_graph_attr(g1,'weight',as2)
#graph_attr(g1,'weight')
E(gm)
E(gm)$weight
E(gm)$weight<-g1weight
#get the region
region<-read.csv('boro_precinct2.csv',header=F)
region <- region[-1,]
head(region)
# make the edge and the node in the same region the same region value
V(gf)$region<-region$V1
for(i in 1:254){
  a = ends(gf, i)[1]
  b = ends(gf, i)[2]
  for (j in V(gf)){
    if(V(gf)[j]$name==a){
      for(k in V(g1)){
        if(V(gf)[k]$name==b){
          E(gf)[i]$region<-V(gf)[j]$region
        } 
      }
    }
  }
}

graph.density(gm)
criminal_rate<-read.csv('level_network/misdemeanor_rate.csv')
head(criminal_rate)
V(gm)$osize<-criminal_rate$crime.thousand_people
par(mar = c(0, 2, 0, 0))
V(gm)$osize

#calculate teh community
vertex_attr(gm)
edge_attr(gm)
cl <- optimal.community(gm)
V(gm)$community <- cl$membership

#------------------violation---------------------
matrixv=read.csv('level_network/violation_unweighted.csv',header=T)

a<-matrixv$X0
rownames(matrixv)<-a
matrixv<-subset(matrixv,select =-X0)
colnames(matrixv)<-a
as<-as.matrix(matrixv)

gv <- graph.adjacency(as, mode = "undirected")
gv<-simplify(gv)

matrixv2<-read.csv('level_network/violation_similarity.csv')
b<-matrixv2$X0
rownames(matrixv2)<-b
matrixv2<-subset(matrixv2,select =-X0)
colnames(matrixv2)<-b

# get the weight of the plot
g1weight<- as.list(matrixv2)
g1weight<-unlist(g1weight)
g1weight<-g1weight[g1weight!=0]

#as2<-as.matrix(matrix2)
#g1<-set_graph_attr(g1,'weight',as2)
#graph_attr(g1,'weight')
E(gv)
E(gv)$weight
E(gv)$weight<-g1weight
#get the region
region<-read.csv('boro_precinct2.csv',header=F)
region <- region[-1,]
head(region)
# make the edge and the node in the same region the same region value
V(gv)$region<-region$V1
for(i in 1:254){
  a = ends(gf, i)[1]
  b = ends(gf, i)[2]
  for (j in V(gf)){
    if(V(gf)[j]$name==a){
      for(k in V(g1)){
        if(V(gf)[k]$name==b){
          E(gf)[i]$region<-V(gf)[j]$region
        } 
      }
    }
  }
}

graph.density(gv)
criminal_rate<-read.csv('level_network/violation_rate.csv')
head(criminal_rate)
V(gv)$osize<-criminal_rate$crime.thousand_people
par(mar = c(0, 2, 0, 0))
V(gv)$osize

#calculate teh community
vertex_attr(gm)
edge_attr(gm)
cl <- optimal.community(gm)
V(gm)$community <- cl$membership


QAP_test <- function(m1, m2 , n_run = 10000) {
  observed_cor <- cor(c(m1), c(m2))
  # initialize the vector to store the correlations for each permutation
  permuted_corr_vector <- rep(0, n_run) 
  for(i in 1:n_run){
    permuted_ids <- sample(nrow(m1), replace = F)
    permuted_corr <- cor(c(m1[permuted_ids, permuted_ids]), c(m2))
    permuted_corr_vector[i] <- permuted_corr
  }
  #QAP p-value
  plot(hist(permuted_corr_vector))
  sum(permuted_corr_vector >= observed_cor)/n_run
}
ma2 <- as.matrix(matrix2)
maf2 <- as.matrix(matrixf2)
mam2 <- as.matrix(matrixm2)
mav2 <- as.matrix(matrixv2)
cor.test(ma2,maf2)
QAP_test(ma2, maf2)
QAP_test(ma2,mam2)
QAP_test(ma2,mav2)

QAP_test(maf2,mam2)
QAP_test(maf2,mav2)
QAP_test(mam2,mav2)
