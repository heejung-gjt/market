from django import template


register = template.Library()

@register.filter
def comment_sum(comment):
  cnt = 0
  for recomment in comment:
    cnt += recomment.re_comment.prefetch_related('comment').all().count()
  sum = comment.count() + cnt
  return sum