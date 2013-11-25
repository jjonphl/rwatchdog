library(RCurl)
library(httr)

url <- "http://localhost:8080/publish"
md.file <- fileUpload("data-doc.Rmd")
data.file1 <- fileUpload("2009-GAA.csv")
data.file2 <- fileUpload("2009-NA.csv")
data.file3 <- fileUpload("2013-GAA.csv")
POST(url, body=list(tw_handle="@jjonphl", md_file=md.file, "data_file"=data.file1, "data_file"=data.file2, "data_file"=data.file3))


POST(url, body=list(tw_handle="@jjonphl", md_file=fileUpload("saob-doc.Rmd"), data_file=fileUpload("2013-SAOB.csv")))

GET("http://localhost:8080/status?uuid=19764673-017c-400b-a457-0fa1c04f83ad")
