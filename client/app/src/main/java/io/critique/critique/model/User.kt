package io.critique.critique.model

import android.util.Log
import com.github.kittinunf.fuel.core.FuelError
import com.github.kittinunf.fuel.httpGet
import com.github.kittinunf.fuel.httpPost
import com.github.kittinunf.fuel.httpPut
import com.github.kittinunf.result.Result
import com.google.gson.Gson
import com.google.gson.JsonElement
import com.google.gson.JsonObject
import com.google.gson.annotations.SerializedName
import io.critique.critique.Globals
import io.critique.critique.Globals.Companion.API_USERS_URL

/**
 * User model class as defined in API.
 */
data class User(
        val nickname: String = "",
        var givenName: String? = "",
        var familyName: String? = null,
        var avatar: String? = null,
        var bio: String? = null,
        var email: String? = "",
        var birthdate: String? = null,
        var telephone: String? = null,
        var gender: String? = null,
        @SerializedName("@controls")
        private val controls: JsonObject = JsonObject()
) {

    val ratings: ArrayList<Rating> = ArrayList()
    val river: ArrayList<Post> = ArrayList()
    val inbox: ArrayList<Post> = ArrayList()

    var onChange: (() -> Unit)? = null

    companion object {
        /**
         * Create User object from json string.
         */
        fun fromJson(json: String): User = Gson().fromJson(json, User::class.java)

        /**
         * Create User object from JsonElement.
         */
        fun fromJson(json: JsonElement): User = Gson().fromJson(json, User::class.java)

        /**
         * Get user API link.
         */
        fun getUserURL(nickname: String): String = "$API_USERS_URL/$nickname"
    }

    /**
     * Convert this user to json string.
     */
    fun toJson(): String = Gson().toJson(this)

    /**
     * Get user river link from the controls.
     */
    fun getRiverURL(): String? = if (controls.has("critique:user-river"))
        Globals.API_URL + controls.get("critique:user-river").asJsonObject.get("href").asString
    else null

    /**
     * Get user inbox link from the controls.
     */
    fun getInboxURL(): String? = if (controls.has("critique:user-inbox"))
        Globals.API_URL + controls.get("critique:user-inbox").asJsonObject.get("href").asString
    else null

    /**
     * Get user ratings link from the controls.
     */
    fun getRatingsURL(): String? = if (controls.has("critique:user-ratings"))
        Globals.API_URL + controls.get("critique:user-ratings").asJsonObject.get("href").asString
    else null

    /**
     * Get edit user link from the controls.
     */
    fun getEditUserURL(): String? = if (controls.has("edit"))
        Globals.API_URL + controls.get("edit").asJsonObject.get("href").asString
    else null

    /**
     * returns default avatar path.
     */
    fun getAvatarPath() = "avatars/$nickname.jpeg"

    /**
     * Parse a json string.
     */
    private fun parse(data: String): JsonObject? = Gson().fromJson(data, JsonObject::class.java)

    /**
     * Query the ratings of the user.
     *
     * @param block: gets called after the query finishes.
     */
    fun queryRatings(block: (ArrayList<Rating>) -> Unit) {
        val url = getRatingsURL()

        if (url != null) {
            url.httpGet().responseString { req, resp, result ->
                when (result) {
                    is Result.Failure -> {
                        // Just print the stacktrace
                        result.error.printStackTrace()
                    }
                    is Result.Success -> {
                        val data = result.get()

                        ratings.clear()

                        parse(data)?.get("items")?.asJsonArray?.forEach {
                            val rating = Rating.fromJson(it)
                            if (rating != null)
                                ratings.add(rating)
                        }

                        block(ratings)
                    }
                }
            }
        } else {
            // pretend it returned empty list
            block(ArrayList())
            Log.e("User", "Ratings url returned null.")
        }
    }

    /**
     * Query the river of the user.
     *
     * @param block: gets called after the query finishes.
     */
    fun queryRiver(block: (ArrayList<Post>) -> Unit) {
        val url = getRiverURL()
        if (url != null) {
            url.httpGet().responseString { req, resp, result ->
                when (result) {
                    is Result.Failure -> {
                        // Just print the stacktrace
                        result.getException().printStackTrace()
                    }
                    is Result.Success -> {
                        val data = result.get()

                        river.clear()

                        parse(data)?.get("items")?.asJsonArray?.forEach {
                            river.add(Post.fromJson(it))
                        }

                        block(river)
                    }
                }
            }
        } else {
            // pretend it returned empty list
            block(ArrayList())
            Log.e("User", "River url returned null.")
        }
    }

    /**
     * Query the inbox of the user.
     *
     * @param block: gets called after the query finishes.
     */
    fun queryInbox(block: (ArrayList<Post>) -> Unit) {
        val url = getInboxURL()
        if (url != null) {
            url.httpGet().responseString { req, resp, result ->
                when (result) {
                    is Result.Failure -> {
                        result.getException().printStackTrace()
                    }
                    is Result.Success -> {
                        val data = result.get()

                        inbox.clear()

                        parse(data)?.get("items")?.asJsonArray?.forEach {
                            inbox.add(Post.fromJson(it))
                        }

                        block(inbox)
                    }
                }
            }
        } else {
            // pretend it returned empty list
            block(ArrayList())
            Log.e("User", "Inbox url returned null.")
        }
    }

    /**
     * Attempt to update user.
     *
     * @param success: gets called when it is successful.
     * @param fail: gets called when fails to updated.
     */
    fun updateUser(editedUser: User, success: () -> Unit, fail: (FuelError?) -> Unit) {
        val url = getEditUserURL()
        if (url != null) {
            url.httpPut()
                    .header(Pair("Content-Type", "application/json"))
                    .body(editedUser.toJson())
                    .responseString { req, resp, result ->
                        when (result) {
                            is Result.Failure -> {
                                fail(result.error)
                            }
                            is Result.Success -> {
                                givenName = editedUser.givenName
                                familyName = editedUser.familyName
                                bio = editedUser.bio
                                telephone = editedUser.telephone
                                gender = editedUser.gender
                                birthdate = editedUser.birthdate
                                avatar = editedUser.avatar

                                onChange?.invoke()
                                success()
                            }
                        }
                    }
        } else {
            fail(null)
        }
    }

    /**
     * Attempt to create user.
     *
     * @param success: gets called when it is successful.
     * @param fail: gets called when fails to create.
     */
    fun createUser(success: () -> Unit, fail: (FuelError) -> Unit) {
        "$API_USERS_URL/".httpPost()
                .header(Pair("Content-Type", "application/json"))
                .body(this.toJson())
                .responseString { req, resp, result ->
                    when (result) {
                        is Result.Failure -> {
                            fail(result.error)
                        }
                        is Result.Success -> {
                            success()
                        }
                    }
                }
    }
}