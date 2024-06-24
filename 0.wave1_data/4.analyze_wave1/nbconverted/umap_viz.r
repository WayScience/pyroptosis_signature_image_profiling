suppressPackageStartupMessages(library(dplyr))
suppressPackageStartupMessages(library(ggplot2))

umap_file <- file.path("results", "umap_embeddings_dilation50.csv.gz")
umap_df <- readr::read_csv(umap_file, show_col_types = FALSE) %>%
    dplyr::mutate(
        translocation_ratio = (
            TranslocatedNuclei_Intensity_IntegratedIntensity_CorrGasderminD /
            DilatedNuclei_Intensity_IntegratedIntensity_CorrGasderminD
            )
        )

print(dim(umap_df))
head(umap_df, 3)

umap_gg <- (
    ggplot(umap_df, aes(x = UMAP0, y=UMAP1))
    + geom_point(
        aes(color = translocation_ratio),
        show.legend = TRUE,
        alpha = 0.2,
        size = 0.5
    )
    + theme_bw()
    + facet_wrap("~Metadata_treatment")
    + scale_color_gradientn(
        name = "Translocation\nratio",
        colors = c("cyan", "black", "red"),
        values = c(0, 0.6, 0.7, 0.8, 0.9, 0.95, 1)
    )
)

output_file <- file.path("figures", "umap_dilation50.png")
ggsave(output_file, umap_gg, height = 4, width = 6, dpi = 500)
umap_gg
