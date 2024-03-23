from abc import ABC
from .exceptions import CountryNotFoundException
import io
from shapely.geometry import shape, Polygon, MultiPolygon
from shapely.ops import unary_union
import shapely
import geopandas as gpd
import matplotlib.pyplot as plt
import orjson


class BaseImageService(ABC):
    def find_feature_by_country_gdf_as_geojson(self, country_name, gdf) -> dict:
        """
        Searches for features in a GeoDataFrame where the 'sovereignt'
        column matches the given country name and returns the matching features as GeoJSON.
        Raises an error if no matching feature is found.

        Parameters:
        - country_name: A string representing the name of the country.
        - gdf: A GeoDataFrame containing the feature collection.

        Returns:
        - A Geojson with The matching country as a feature.

        Raises:
        - CountryNotFoundException: If no matching feature is found.
        """
        formatted_country_name = country_name.lower().capitalize()

        matching_features = gdf[gdf["sovereignt"] == formatted_country_name]

        if matching_features.empty:
            raise CountryNotFoundException(
                f"No matching countries under the sovereignt of: {formatted_country_name}",
            )

        matching_features_geojson = matching_features.to_json()
        return orjson.loads(matching_features_geojson)

    def clean_canvas(self, ax):
        """Removes the frame, ticks, and spines from a Matplotlib axis."""
        ax.set_frame_on(False)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.get_xaxis().set_ticks([])
        ax.get_yaxis().set_ticks([])

    def plot_geojson_and_save(
        self,
        geojson_data: dict,
        text: str,
        text_position=(0.01, 0.99),
        text_kwargs=None,
    ) -> io.BytesIO:
        """
        Plots GeoJSON data, adds optional text, and saves it to a file.

        Parameters:
        - geojson_data: A GeoJSON object representing geographic data.
        - filename: The name of the file where the plot will be saved. Default is 'geojson_plot.png'.
        - text: Optional text to add to the plot. If None, no text is added.
        - text_position: A tuple (x, y) specifying the position of the text. Coordinates are relative to the plot's axes (from 0 to 1).
        - text_kwargs: A dictionary of keyword arguments to customize the appearance of the text. Check matplotlib's `text` documentation for available options.
        """
        # Convert the GeoJSON data to a GeoDataFrame
        gdf = gpd.GeoDataFrame.from_features(geojson_data)

        # Plotting
        fig, ax = plt.subplots(figsize=(10, 10))  # Adjust the size as needed
        gdf.plot(ax=ax)

        if text is not None:
            default_text_kwargs = {
                "fontsize": 60,
                "fontweight": "bold",
                "fontname": "Arial",
                "color": "black",
                "ha": "left",
                "va": "top",
            }
            text_kwargs = text_kwargs or {}
            default_text_kwargs.update(text_kwargs)
            ax.text(
                text_position[0],
                text_position[1],
                text,
                transform=ax.transAxes,
                **default_text_kwargs,
            )

        self.clean_canvas(ax)
        buf = io.BytesIO()
        plt.savefig(buf, format="png", bbox_inches="tight")
        plt.close()  # Close the plot to free memory
        buf.seek(0)
        return buf


class ImageService(BaseImageService):
    def __init__(self, world_file_path: str = "data/world.geojson"):
        self.world_geojson = self.load_feature_collection(world_file_path)

    def load_feature_collection(self, geojson_path) -> gpd.GeoDataFrame:
        """
        Loads a feature collection from a GeoJSON file.

        Parameters:
        - geojson_path: The file path to the GeoJSON file.

        Returns:
        - A GeoDataFrame containing the features from the GeoJSON file.
        """
        gdf = gpd.read_file(geojson_path)
        return gdf

    def get_country_image(
        self,
        country_name: str,
        buffer,
        simplify: float,
    ) -> io.BytesIO:
        geojson_feature = self.find_feature_by_country_gdf_as_geojson(
            country_name,
            self.world_geojson,
        )
        country_geom: Polygon | MultiPolygon = shape(
            geojson_feature["features"][0]["geometry"],
        )

        if isinstance(country_geom, Polygon):
            country_geom = country_geom.buffer(buffer).simplify(simplify)
        else:
            country_geom = unary_union(
                [g.buffer(buffer).simplify(simplify) for g in country_geom.geoms],
            )

        geojson_feature["features"][0]["geometry"] = orjson.loads(
            shapely.to_geojson(country_geom),
        )
        country_image_buffer = self.plot_geojson_and_save(
            geojson_feature,
            text=country_name,
        )
        return country_image_buffer
