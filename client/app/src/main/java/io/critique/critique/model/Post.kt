package io.critique.critique.model

import com.github.kittinunf.fuel.core.FuelError
import com.github.kittinunf.fuel.httpDelete
import com.github.kittinunf.fuel.httpPut
import com.github.kittinunf.result.Result
import com.google.gson.Gson
import com.google.gson.JsonElement
import com.google.gson.JsonObject
import com.google.gson.annotations.SerializedName
import io.critique.critique.Globals

/**
 * Post model object as defined in the API.
 */
data class Post(
        val sender: String = "",
        val receiver: String? = null,
        val timestamp: Long = 0L,
        val postId: String = "",
        val replyTo: String? = null,
        var body: String = "",
        @SerializedName("anonymous")
        private var anonymousInt: Int = 1,
        @SerializedName("public")
        private var publicInt: Int = 1,
        val bestRating: Int = 10,
        var ratingValue: Int? = 0,
        val image: String? = null,
        @SerializedName("@controls")
        val controls: JsonObject = JsonObject()
) {

    /**
     * Get the json string of this object.
     */
    fun toJson(): String = Gson().toJson(this)

    /**
     * Get delete post URL from controls
     */
    fun getDeletePostURL(): String? = getControlLink("critique:delete")

    /**
     * get edit post URL from controls
     */
    fun getEditPostURL(): String? = getControlLink("edit")

    /**
     * get sender of the post URL from controls
     */
    fun getSenderURL(): String? = getControlLink("critique:sender")

    /**
     * helper function for getting a control
     */
    private fun getControlLink(name: String): String? = if (controls.has(name))
        Globals.API_URL + controls.get(name).asJsonObject.get("href").asString
    else null

    var anonymous: Boolean
        get() = anonymousInt == 1
        set(value) {
            anonymousInt = if (value) 1 else 0
        }

    var public: Boolean
        get() = publicInt == 1
        set(value) {
            publicInt = if (value) 1 else 0
        }

    companion object {
        /**
         * create a post object from json string
         */
        fun fromJson(json: String): Post = Gson().fromJson(json, Post::class.java)

        /**
         * create a post object from JsonElement
         */
        fun fromJson(json: JsonElement): Post = Gson().fromJson(json, Post::class.java)
    }

    /**
     * Attempt to edit the post with the given new version.
     *
     * @param editedPost: the post to be edited
     * @param success: gets called when it is successful.
     * @param fail: gets called when fails to updated.
     */
    fun edit(editedPost: Post, success: () -> Unit, fail: (FuelError?) -> Unit) {
        if (editedPost.postId != postId)
            fail(null)

        val url = getEditPostURL()
        if (url != null) {
            val json = editedPost.toJson()
            url.httpPut()
                    .header(Pair("Content-Type", "application/json"))
                    .body(json)
                    .responseString { request, response, result ->
                        when (result) {
                            is Result.Failure -> {
                                fail(result.error)
                            }
                            is Result.Success -> {
                                body = editedPost.body
                                public = editedPost.public
                                ratingValue = editedPost.ratingValue

                                success()
                            }
                        }
                    }
        } else {
            fail(null)
        }
    }

    /**
     * Attempt to delete this post.
     *
     * @param success: gets called when it is successful.
     * @param fail: gets called when fails to delete.
     */
    fun delete(success: () -> Unit, fail: (FuelError?) -> Unit) {
        val url = getDeletePostURL()
        if (url != null) {
            url.httpDelete().responseString { request, response, result ->
                when (result) {
                    is Result.Failure -> {
                        fail(result.error)
                    }
                    is Result.Success -> {
                        success()
                    }
                }
            }
        } else {
            fail(null)
        }
    }
}