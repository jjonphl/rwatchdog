library(twitteR)

cacert <- system.file("CurlSSL/cacert.pem", package="RCurl")
options(RCurlOptions=list(cainfo=cacert))


# first time cred
if (!file.exists("twitter-cred.rda")) {
  cred <- getTwitterOAuth(consumer_key="3JFVbIwU50Er0bix9qlXRA",
                          consumer_secret="HMg2S0tFWctlLOJjzlP8WGZij6z6ilxY8WZ02Y1u0")

  save(cred, file="twitter-cred.rda")
} else {
  load("twitter-cred.rda")
}

registerTwitterOAuth(cred)
tweet("Test message")

img <- readBin("figure/unnamed-chunk-1.png", "raw")

tweetImage("Test image", img)
