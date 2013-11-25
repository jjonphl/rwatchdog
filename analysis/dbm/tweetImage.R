tweetImage <- function (text, img, lat = NULL, long = NULL, placeID = NULL, displayCoords = NULL, 
                        inReplyTo = NULL, ...) {
  if (!twitteR:::hasOAuth()) 
    stop("updateStatus requires OAuth authentication")
  if (nchar(text) > 140) 
    stop("Status can not be more than 140 characters")
  params = twitteR:::buildCommonArgs(lat = lat, long = long, place_id = placeID, 
                                     display_coordinates = displayCoords, in_reply_to_status_id = inReplyTo)
  params[["status"]] <- text
  #params[["media[]"]] <- img
  json = twitteR:::twInterfaceObj$doAPICall("statuses/update_with_media", params = params, 
                                            method = "POST", ...)
  return(twitteR:::buildStatus(json))
}