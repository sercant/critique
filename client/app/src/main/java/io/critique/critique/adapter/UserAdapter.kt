package io.critique.critique.adapter

import android.content.Context
import android.content.Intent
import android.support.v7.widget.CardView
import android.support.v7.widget.RecyclerView
import android.view.LayoutInflater
import android.view.ViewGroup
import io.critique.critique.ProfileActivity
import io.critique.critique.R
import io.critique.critique.helper.FirebaseHelper
import io.critique.critique.model.User
import kotlinx.android.synthetic.main.user_card.view.*
import org.ocpsoft.prettytime.PrettyTime

/**
 * Updates the items in the recycle view
 */
class UserAdapter(private val data: List<User>) :
        RecyclerView.Adapter<UserAdapter.ViewHolder>() {

    private val prettyTime = PrettyTime()

    // Provide a reference to the views for each data item
    // Complex data items may need more than one view per item, and
    // you provide access to all the views for a data item in a view holder.
    // Each data item is just a string in this case that is shown in a TextView.
    class ViewHolder(val cardView: CardView) : RecyclerView.ViewHolder(cardView)


    // Create new views (invoked by the layout manager)
    override fun onCreateViewHolder(parent: ViewGroup,
                                    viewType: Int): ViewHolder {
        // create a new view
        val cardView = LayoutInflater.from(parent.context)
                .inflate(R.layout.user_card, parent, false) as CardView
        // set the view's size, margins, paddings and layout parameters
//        ...
        return ViewHolder(cardView)
    }

    // Replace the contents of a view (invoked by the layout manager)
    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        // - get element from your dataset at this position
        // - replace the contents of the view with that element
        holder.cardView.apply {
            val user = data[position]

            nickname.text = user.nickname

            user.avatar?.let {
                FirebaseHelper.getImageFromStorage(it, {
                    if (it != null)
                        avatar.setImageBitmap(it)
                    else
                        avatar.setImageResource(R.drawable.ic_account_circle_black_24dp)
                })
            }

            bio.text = user.bio

            setOnClickListener {
                openProfile(context, user.nickname)
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