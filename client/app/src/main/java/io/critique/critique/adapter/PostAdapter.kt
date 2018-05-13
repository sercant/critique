package io.critique.critique.adapter

import android.content.Context
import android.content.Intent
import android.support.v7.widget.CardView
import android.support.v7.widget.RecyclerView
import android.view.LayoutInflater
import android.view.View.GONE
import android.view.View.VISIBLE
import android.view.ViewGroup
import android.widget.Toast
import com.bumptech.glide.Glide
import com.github.kittinunf.fuel.httpGet
import com.github.kittinunf.result.Result
import io.critique.critique.Events
import io.critique.critique.Globals
import io.critique.critique.ProfileActivity
import io.critique.critique.R
import io.critique.critique.helper.FirebaseHelper
import io.critique.critique.model.Post
import io.critique.critique.model.Rating
import io.critique.critique.model.User
import kotlinx.android.synthetic.main.post_card.view.*
import org.ocpsoft.prettytime.PrettyTime
import java.util.*

/**
 * Updates the items in the recycle view
 */
class PostAdapter(private val data: ArrayList<Post>) :
        RecyclerView.Adapter<PostAdapter.ViewHolder>() {

    private val prettyTime = PrettyTime()

    // Provide a reference to the views for each data item
    // Complex data items may need more than one view per item, and
    // you provide access to all the views for a data item in a view holder.
    // Each data item is just a string in this case that is shown in a TextView.
    class ViewHolder(val cardView: CardView) : RecyclerView.ViewHolder(cardView)


    // Create new views (invoked by the layout manager)
    override fun onCreateViewHolder(parent: ViewGroup,
                                    viewType: Int): PostAdapter.ViewHolder {
        // create a new view
        val cardView = LayoutInflater.from(parent.context)
                .inflate(R.layout.post_card, parent, false) as CardView
        // set the view's size, margins, paddings and layout parameters
//        ...
        return ViewHolder(cardView)
    }

    // Replace the contents of a view (invoked by the layout manager)
    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        // - get element from your dataset at this position
        // - replace the contents of the view with that element
        holder.cardView.apply {
            val post = data[position]

            body.text = post.body
            sender.apply {
                text = if (post.anonymous) "Anonymous" else post.sender
                setOnClickListener {
                    if (!post.anonymous) openProfile(context, post.sender)
                }
            }

            if (post.receiver != null) {
                receiver.apply {
                    text = post.receiver
                    setOnClickListener {
                        openProfile(context, post.receiver)
                    }
                }

                post_caret.visibility = VISIBLE
            } else {
                receiver.visibility = GONE
                post_caret.visibility = GONE
            }

            holder.cardView.setOnClickListener {

            }

            if (post.image != null) {
                image.visibility = VISIBLE
                image.setOnClickListener {
                    openProfile(context, post.sender)
                }

                Glide.with(context)
                        .load(post.image)
                        .into(image)
            } else {
                image.visibility = GONE
            }

            avatar.setImageResource(R.drawable.ic_account_circle_black_24dp)
            // attempt to set the avatar of the sender.
            if (!post.anonymous) {
                avatar.setOnClickListener {
                    openProfile(context, post.sender)
                }

                post.getSenderURL()?.httpGet()?.responseString { _, _, result ->
                    when (result) {
                        is Result.Failure -> {
                            // couldn't load the user for avatar. no big deal ignore it.
                            result.error.exception.printStackTrace()
                        }
                        is Result.Success -> {
                            val senderUser = User.fromJson(result.get())
                            senderUser.avatar?.let {
                                if (!it.isBlank())
                                    FirebaseHelper.getImageFromStorage(it, {
                                        it ?: return@getImageFromStorage

                                        avatar.setImageBitmap(it)
                                    })
                            }
                        }
                    }
                }
            }

            day.text = prettyTime.format(Date(System.currentTimeMillis() - post.timestamp))

            if (post.ratingValue?.let {
                        post.ratingValue?.let {
                            rating.rating = it.div(post.bestRating.toFloat()) * Rating.BEST_RATING
                            rating.visibility = VISIBLE
                        }
                        true
                    } != true) {
                rating.visibility = GONE
            }


            if (post.receiver == Globals.myUser.nickname) {
                inbox_controls.visibility = VISIBLE

                if (!post.public) {
                    publish_button.visibility = VISIBLE

                    publish_button.setOnClickListener {
                        val editedPost = post.copy()
                        editedPost.public = true

                        post.edit(editedPost, {
                            notifyDataSetChanged()
                            data.remove(post)
                            notifyDataSetChanged()

                            context.sendBroadcast(Intent(Events.ACTION_POST_PUBLISH))
                        }, {
                            Toast.makeText(context, if (it != null) String(it.errorData) else "Unknown Error", Toast.LENGTH_SHORT).show()
                        })
                    }
                } else {
                    publish_button.visibility = GONE
                }

                delete_button.setOnClickListener {
                    post.delete({
                        data.remove(post)
                        notifyDataSetChanged()

                        context.sendBroadcast(Intent(Events.ACTION_POST_DELETE))
                    }, {
                        Toast.makeText(context, if (it != null) String(it.errorData) else "Unknown Error", Toast.LENGTH_SHORT).show()
                    })
                }
            } else {
                inbox_controls.visibility = GONE
            }
        }
    }

    /**
     * Open profile of the clicked person
     */
    private fun openProfile(context: Context, nickname: String) {
        val intent = Intent(context, ProfileActivity::class.java).apply {
            putExtra(ProfileActivity.EXTRA_NICKNAME, nickname)
        }
        context.startActivity(intent)
    }

    // Return the size of your data (invoked by the layout manager)
    override fun getItemCount() = data.size
}