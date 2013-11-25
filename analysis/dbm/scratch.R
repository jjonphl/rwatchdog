x <- read.csv("2013-SARO.csv")

gaa.2009 <- read.csv("2009-GAA.csv")[-1,]

extract.codes <- function(data) {
  dept <- unique(data[,c("DPT_CD","DPT_DSC")])
  dept <- dept[order(dept[,1]),]
  
  owner <- unique(data[,c("OWNER_CD","OWNER_DSC")])
  owner <- owner[order(owner[,1]),]
  
  fpap <- unique(data[,c("FPAP_CD","FPAP_DSC")])
  fpap <- fpap[order(fpap[,1]),]
  
  area <- unique(data[,c("AREA_CD","AREA_DSC")])
  area <- area[order(area[,1]),]
  
  agency <- sort(unique(data[,"AGY_TYPE"]))
  
  agency2 <- unique(data[,c("AGY_TYPE", "AREA_CD","AREA_DSC")])
  agency2 <- agency2[order(agency2[,2]),]
  
  list(dept=dept, owner=owner, fpap=fpap, area=area, agency=agency, agency2=agency2)
}

sapply(str_split(head(gaa.2009$FPAP_CD),"\\."), function(x) length(x) == 2)

idx <- sapply(str_split(gaa.2009$FPAP_CD,"\\."), function(x) length(x) == 2)
x0 <- gaa.2009[idx,c("DPT_CD","DPT_DSC","OWNER_CD","OWNER_DSC","FPAP_CD","FPAP_DSC")]

fpap <- unique(x0[,c("FPAP_CD","FPAP_DSC")])
fpap <- fpap[order(fpap[,"FPAP_CD"]),]


saob <- read.csv("2013-SAOB.csv")
names(saob)
