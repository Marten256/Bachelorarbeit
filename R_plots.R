#resistance
data_txt<- read.table('/homes/marten/Schreibtisch/Combined/rgi/Vergleich/übereinstimmung_und_widerspruch_beim_vergleich_RGI2_Resistance_R_angepasst.txt', sep = '\t', header = TRUE)

ggplot(data=data_txt, aes(x=RESISTANCE.Antibiotics, y=Quantity, fill=factor(Übereinstimmung.1..Wiederspruch.2.)))+
    geom_bar(color = 'black', stat = 'identity', position = 'stack', width = 0.8)+
    labs(y = 'Frequency', x = 'Antibiotic', fill = 'RGI prediction')+
    scale_fill_manual(values = c('red', 'steelblue'))+
    ggtitle('True and false prediction of the adjusted program for resistances to antibiotics using RGI data')+
    theme(plot.title = element_text(hjust = 0.5, size = 16), axis.title.y = element_text(size = 14), axis.title.x = element_text(size = 14), axis.text.y = element_text(size = 9))+
    coord_flip()+
    scale_y_continuous(breaks = seq(0, 40, 5))
ggsave("/homes/marten/Schreibtisch/Combined/rgi/pngs/True_and_false_prediction_of_the_adjusted_program_for_resistances.png")

#mediate
data_txt<- read.table('/homes/marten/Schreibtisch/Combined/rgi/Vergleich/übereinstimmung_und_widerspruch_beim_vergleich_RGI2_Mediate_R_angepasst.txt', sep = '\t', header = TRUE)

ggplot(data=data_txt, aes(x=MEDIATE.Antibiotics, y=Quantity, fill=factor(Übereinstimmung.1..Wiederspruch.2.)))+
    geom_bar(color = 'black', stat = 'identity', position = 'stack', width = 0.8)+
    labs(y = 'Frequency', x = 'Antibiotic', fill = 'RGI prediction')+
    scale_fill_manual(values = c('red', 'steelblue'))+
    ggtitle('True and false prediction of the adjusted program for mediate behavior to antibiotics using RGI data')+
    theme(plot.title = element_text(hjust = 0.5, size = 16), axis.title.y = element_text(size = 14), axis.title.x = element_text(size = 14), axis.text.y = element_text(size = 9))+
    coord_flip()+
    scale_y_continuous(breaks = seq(0, 40, 5))
  ggsave("/homes/marten/Schreibtisch/Combined/rgi/pngs/True_and_false_prediction_of_the_adjusted_program_for_mediate_behavior.png")

#sensitive
data_txt<- read.table('/homes/marten/Schreibtisch/Combined/rgi/Vergleich/übereinstimmung_und_widerspruch_beim_vergleich_RGI2_Sensitive_R_angepasst.txt', sep = '\t', header = TRUE)

ggplot(data=data_txt, aes(x=SENSITIVE.Antibiotics, y=Quantity, fill=factor(Übereinstimmung.1..Wiederspruch.2.)))+
    geom_bar(color = 'black', stat = 'identity', position = 'stack', width = 0.8)+
    labs(y = 'Frequency', x = 'Antibiotic', fill = 'RGI prediction')+
    scale_fill_manual(values = c('red', 'steelblue'))+
    ggtitle('True and false prediction of the adjusted program for sensitive behavior to antibiotics using RGI data')+
    theme(plot.title = element_text(hjust = 0.5, size = 16), axis.title.y = element_text(size = 14), axis.title.x = element_text(size = 14), axis.text.y = element_text(size = 9))+
    coord_flip()+
    scale_y_continuous(breaks = seq(0, 70, 5))
ggsave("/homes/marten/Schreibtisch/Combined/rgi/pngs/True_and_false_prediction_of_the_adjusted_program_for_sensitive_behavior.png")

#Vergleich resistant und sensitive
data_txt<- read.table('/homes/marten/Schreibtisch/Combined/rgi/Vergleich/übereinstimmung_und_widerspruch_beim_vergleich_RGI2_Resistance_R_r_s_vergleich.txt', sep = '\t', header = TRUE)


myplot <- ggplot(data=data_txt, aes(x=RESISTANCEorSENSITIV, y=Quantity, fill=factor(True.False.positive.negative)))+
    geom_bar(color = 'black', stat = 'identity', position = 'stack', width = 0.8)+
    labs(y = 'Frequency', x = 'Antibiotic', fill = 'RGI prediction')+
    scale_fill_manual(values = c('steelblue', 'darkcyan', 'orange', 'yellow'))+
    ggtitle('Comparison of the predictions for resistant and sensitve behavior')+
    theme(plot.title = element_text(hjust = 0.5, size = 16), axis.title.y = element_text(size = 14), axis.title.x = element_text(size = 14), axis.text.y = element_text(size = 9))+
    coord_flip()+
    scale_y_continuous(breaks = seq(0, 90, 5))
ggsave("/homes/marten/Schreibtisch/Combined/rgi/pngs/Comparison_of_the_predictions_for_resisant_and_sensitve_behavior.png")


