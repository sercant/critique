package io.critique.critique.model

import com.google.gson.Gson
import com.google.gson.annotations.SerializedName

/**
 * Error model class as defined in the error profile of the API.
 */
data class Error(
        @SerializedName("@error")
        val error: ErrorBody = ErrorBody(),

        @SerializedName("resource_url")
        val resourceUrl: String = ""
) {

    /**
     * Internal class for error body representation
     */
    data class ErrorBody(
            @SerializedName("@message")
            val message: String = "Unknown Error"
    )

    companion object {
        /**
         * Convert to Error object from ByteArray
         */
        fun fromError(message: String?, data: ByteArray?): Error =
                if (data != null && data.isNotEmpty())
                    fromJson(String(data))
                else if (message != null && !message.isBlank())
                    Error(error = ErrorBody(message))
                else
                    Error()

        /**
         * Convert to Error object from String
         */
        fun fromJson(data: String?): Error {
            return try {
                Gson().fromJson(data, Error::class.java)
            } catch (e: Exception) {
                e.printStackTrace()

                if (data != null)
                    Error(error = ErrorBody(data))
                else
                    Error()
            }
        }
    }
}