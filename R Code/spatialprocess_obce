Sys.setlocale(category = "LC_ALL", locale = "cs_CZ.UTF-8")
library(shapefiles)
library(sp)
library(spatstat)
library(maptools)
library(rgdal)
library(OpenStreetMap)
library(DeducerSpatial)

gpclibPermit()

PS10_merged <- dget('/Users/petrbouchal/Documents/Aptana Studio 3 Workspace/Volby_CZ/R Data/PS10_obce.robj')

# OLD WAY TO LOAD SHAPEFILE
#
#x <- readShapeSpatial("/Users/petrbouchal/Documents/Research Projects/Geodata/Okresy_WGS84/okresy", proj=CRS('+proj=longlat +datum=WGS84'))
#x <- spTransform(x, osm())
#geodata <- x@data

#  LOAD SHAPEFILE
setwd("/Users/petrbouchal/Documents/Research Projects/Geodata/Obce_WGS84")
obce = readOGR(dsn=".", layer="obce")
obce@data$id = rownames(obce@data)
obce.points = fortify(obce, region="id")
obce.df = join(obce.points, obce@data, by="id")

# create subset for one party
piece<-subset(PS10_merged,KandidatkaCislo == 24)
piece$KOD_OBEC<-piece$CisloObce
piece<- sort(piece, by=~ KOD_OBCE)
rownames(piece) <-1:dim(piece)[1]
# merge with geodata
obce.df.temp<-obce.df[setdiff(colnames(obce.df),c())]
piece.temp<-piece[setdiff(colnames(piece),c())]
obce.df<-merge(obce.df.temp,piece.temp,by.x=c("KOD_OBEC"),by.y=c("KODE_OBEC"),incomparables = NA,all.x =T,all.y =T)
rm(list=c("obce.df.temp","piece.temp"))

dev.new()
ggplot() +
	geom_polygon(aes(x = long,y = lat,fill = Procenta,group = group),data=obce.df) +
	coord_map() +
	scale_fill_gradient(guide = guide_legend(),low = '#ffe75e',high = '#f52a30')
