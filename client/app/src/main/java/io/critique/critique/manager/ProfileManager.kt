package io.critique.critique.manager

import android.app.Activity
import android.os.Handler
import android.view.View
import com.github.kittinunf.fuel.httpGet
import com.github.kittinunf.result.Result
import io.critique.critique.Globals
import io.critique.critique.helper.FirebaseHelper
import io.critique.critique.model.Rating
import io.critique.critique.model.User
import kotlinx.android.synthetic.main.activity_main.view.*
import kotlinx.android.synthetic.main.profile.view.*

/**
 * Manages the UI of the user profile type of views.
 */
class ProfileManager(
        private val activity: Activity,
        private val view: View,
        private val nickname: String
) {

    var user: User? = null

    var postManager: PostManager? = null

    init {
        // check if the user is our user
        if (Globals.myUser.nickname == nickname) {
            user = Globals.myUser
            init()
        } else {
            // else get it from API
            User.getUserURL(nickname).httpGet().responseString { req, resp, result ->
                when (result) {
                    is Result.Failure -> {
                        result.getException().printStackTrace()
                    }
                    is Result.Success -> {
                        val data = result.get()
                        user = User.fromJson(data)
                        init()
                    }
                }
            }
        }
    }

    fun init() {
        // Initialize required user fields by this view
        user?.apply {
            queryRatings {
                updateRatings()
            }

            queryRiver {
                postManager?.update()
            }

            postManager = PostManager(activity, view.user_river, river)

            onChange = {
                Handler().postDelayed({
                    update()
                }, 1000)
            }
        }

        update()
    }

    /**
     * Update the user info on the visual fields.
     */
    fun update() {
        // Set the user info to the view.
        user?.let {
            view.user_bio.text = it.bio ?: ""

            val name = it.givenName + (if (it.familyName != null) " ${it.familyName}" else "")
            view.user_name.text = name

            it.avatar?.let {
                FirebaseHelper.getImageFromStorage(it, {
                    it ?: return@getImageFromStorage
                    view.user_avatar.setImageBitmap(it)
                })
            }

            postManager?.update()
            updateRatings()
        }
    }

    /**
     * calculates the avarage of the user's ratings
     */
    fun updateRatings() {
        user?.ratings?.let {
            view.rating.rating = (it.sumByDouble { it.ratingValue.div(it.bestRating.toDouble()) } * Rating.BEST_RATING / it.size).toFloat()
        }
    }
}