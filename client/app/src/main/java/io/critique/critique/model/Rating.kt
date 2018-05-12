package io.critique.critique.model

import com.google.gson.Gson
import com.google.gson.JsonElement

/**
 * Rating model as defined in API.
 */
class Rating(
        val sender: String = "",
        val receiver: String = "",
        val bestRating: Int = 10,
        var ratingValue: Int = 0,
        val timestamp: Long = 0L
) {
    companion object {
        const val BEST_RATING: Int = 5

        /**
         * Create rating model from json String.
         */
        fun fromJson(json: String): Rating? = Gson().fromJson(json, Rating::class.java)

        /**
         * Create rating model from JsonElement.
         */
        fun fromJson(element: JsonElement): Rating? = Gson().fromJson(element, Rating::class.java)
    }
}