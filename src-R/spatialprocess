Sys.setlocale(category = "LC_ALL", locale = "cs_CZ.UTF-8")
library(shapefiles)
library(sp)
library(spatstat)
library(maptools)
library(rgdal)
library(OpenStreetMap)
library(DeducerSpatial)

gpclibPermit()

PS10_merged <- dget('/Users/petrbouchal/Documents/Aptana Studio 3 Workspace/Volby_CZ/R Data/PS10_merged.robj')

# BUILD PROPER NUTS CODE FOR DISTRICTS
PS10_merged$first <- substr(PS10_merged$Okres, 1,2)
PS10_merged$last <- substr(PS10_merged$Okres, 4,4)
PS10_merged$NUTS4 <- paste("CZ0",PS10_merged$first, PS10_merged$last, sep="")

# RECODE NUTS4 to merge with geodata
PS10_merged$NUTS4 <- ifelse(PS10_merged$OkresNazev == "P?’bram", "CZ021B", PS10_merged$NUTS4)
PS10_merged$NUTS4 <- ifelse(PS10_merged$OkresNazev == "Rakovn’k", "CZ021C", PS10_merged$NUTS4)
PS10_merged$NUTS4 <- ifelse(PS10_merged$OkresNazev == "Praha-z‡pad", "CZ021A", PS10_merged$NUTS4)

#LOAD SHAPEIFILE
#
#x <- readShapeSpatial("/Users/petrbouchal/Documents/Research Projects/Geodata/Okresy_WGS84/okresy", proj=CRS('+proj=longlat +datum=WGS84'))
#x <- spTransform(x, osm())
#geodata <- x@data

# ALT LOAD
setwd("/Users/petrbouchal/Documents/Research Projects/Geodata/Okresy_WGS84")
okres = readOGR(dsn=".", layer="okresy")
okres@data$id = rownames(okres@data)
okres.points = fortify(okres, region="id")
okres.df = join(okres.points, okres@data, by="id")

# create subset for one party
piece<-subset(PS10_merged,KandidatkaCislo == 24)
piece<- sort(piece, by=~ NUTS4)
rownames(piece) <-1:dim(piece)[1]
# merge with geodata
okres.df.temp<-okres.df[setdiff(colnames(okres.df),c())]
piece.temp<-piece[setdiff(colnames(piece),c())]
okres.df<-merge(okres.df.temp,piece.temp,by.x=c("NUTS4"),by.y=c("NUTS4"),incomparables = NA,all.x =T,all.y =T)
rm(list=c("okres.df.temp","piece.temp"))

dev.new()
ggplot() +
	geom_polygon(aes(x = long,y = lat,fill = Procenta,group = group),data=okres.df) +
	coord_map() +
	scale_fill_gradient(guide = guide_legend(),low = '#ffe75e',high = '#f52a30')
