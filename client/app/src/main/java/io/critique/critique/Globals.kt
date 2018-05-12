package io.critique.critique

import com.github.kittinunf.fuel.httpGet
import com.github.kittinunf.result.Result
import com.google.gson.Gson
import com.google.gson.JsonObject
import io.critique.critique.model.User


/**
 * Global constants and functions for general usage in application
 */
class Globals {

    companion object {

        // URL of the api
        const val API_URL = "http://10.0.2.2:5000"

        // URL of the users resource
        const val API_USERS_URL = "$API_URL/critique/api/users"

        // My user
        var myUser: User = User()

        // List of all users
        val allUsers: ArrayList<User> = ArrayList()

        /**
         * Query the list of all users.
         *
         * @param block: callback on the call finishes.
         */
        fun queryUsers(block: (ArrayList<User>) -> Unit) {
            API_USERS_URL.httpGet().responseString { req, resp, result ->
                when (result) {
                    is Result.Failure -> {
                        result.getException().printStackTrace()
                        allUsers.clear()

                        block(allUsers)
                    }
                    is Result.Success -> {
                        val data = result.get()
                        var users = Gson().fromJson(data, JsonObject::class.java)

                        allUsers.clear()
                        for (user in users.get("items").asJsonArray) {
                            allUsers.add(User.fromJson(user))
                        }

                        block(allUsers)
                    }
                }
            }
        }
    }
}