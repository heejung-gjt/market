from social.models import Like


class SocialService():

  @staticmethod
  def find_clicked_like_article_list(user):
    articles = Like.objects.filter(users__pk = user.pk).all()
    return articles