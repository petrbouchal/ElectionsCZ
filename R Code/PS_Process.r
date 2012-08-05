# NOTE: NEED TO SET LOCALE!! for regex to work with UTF-8:
Sys.setlocale(category = "LC_ALL", locale = "en_GB.UTF-8")

data <- read.table("/Users/petrbouchal/Documents/Aptana Studio 3 Workspace/Volby_CZ/CSVPS/PS_KandidatiKrajeaDetaily.csv",header=T,sep=",",quote="\"", encoding="UTF-8")


data[['veksq']] <- data[['vek']]^2
data$proc <- as.integer(data$Procenta)
data$vek <- as.integer(data$KandVek)
data$bezpartajni <- grepl("BEZPP", data$Prislusnost, ignore.case = TRUE)
data$starosta <- grepl("starost", data$Povolani, ignore.case = TRUE)
data$poslanec <- grepl("poslan", data$Povolani, ignore.case = TRUE)
data$lekar <- grepl("lŽka?", data$Povolani, ignore.case = TRUE)
data$mudr <- grepl("MUDr.", data$KandJmeno, ignore.case = TRUE)
data$ing <- grepl("ing", data$KandJmeno, ignore.case = TRUE)
data$mgr <- grepl("Mg", data$KandJmeno)
data$judr <- grepl("JUDr", data$KandJmeno)
data$zenajmeno <- regexpr("o{1}v{1}‡{1}\\s{1}", data$KandJmeno)
data$zenajmeno <- ifelse(data$zenajmeno>0, 1, 0)

# generate maxima of PocetKand per list & region
data2 <- ddply(data, .(Kandidatka, Kraj), transform, pocetkand = max(PoradiKand))
data2$last4 <- ifelse(data2$PoradiKand > data2$pocetkand - 3, 1, 0)

# clean up data types
data2[,4]<-as.character(data2[,4])
data2[,14]<-as.character(data2[,14])
data2[,23]<-as.integer(data2[,23])
data2[,25]<-as.integer(data2[,25])
data2[,23]<-as.logical(data2[,23])
data2[,25]<-as.logical(data2[,25])

model.lm <- lm(formula = proc ~ PoradiKand + vek + as.factor(Kraj) + as.factor(Kandidatka) + 
    as.factor(bezpartajni) + as.factor(starosta) + as.factor(mudr) + 
    as.factor(ing) + as.factor(mgr) + as.factor(judr) + as.factor(zenajmeno) + 
    as.factor(last4) + as.factor(poslanec), data = data2, na.action = na.omit)
summary(model.lm)
vif(model.lm)

# but use lmer out of lme4 for mixed effects