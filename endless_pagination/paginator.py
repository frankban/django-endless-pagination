from math import ceil

from django.core.paginator import Paginator, Page, EmptyPage, PageNotAnInteger

class CustomPage(Page):
    def start_index(self):
        # Special case, return zero if no items.
        if self.paginator.count == 0:
            return 0
        return max((self.number-2)*self.paginator.per_page + self.paginator.first_page + 1, 
            1)

    def end_index(self):
        # Special case for the last page because there can be orphans.
        if self.number == self.paginator.num_pages:
            return self.paginator.count
        return (self.number-1)*self.paginator.per_page + self.paginator.first_page
        
        
class BasePaginator(Paginator):
    def __init__(self, object_list, per_page, **kwargs):
        if "first_page" in kwargs:
            self.first_page = kwargs.pop("first_page")
        else:
            self.first_page = per_page
        super(BasePaginator, self).__init__(object_list, per_page, **kwargs)
    
    def get_current_per_page(self, number):
        return self.first_page if number == 1 else self.per_page


class DefaultPaginator(BasePaginator):    
    def page(self, number):
        number = self.validate_number(number)
        bottom = max((number-2)*self.per_page + self.first_page, 0)
        top = bottom + self.get_current_per_page(number)
        if top + self.orphans >= self.count:
            top = self.count
        return CustomPage(self.object_list[bottom:top], number, self)
        
    def _get_num_pages(self):
        if self._num_pages is None:
            if self.count == 0 and not self.allow_empty_first_page:
                self._num_pages = 0
            else:
                hits = max(0, self.count - self.orphans - self.first_page)
                self._num_pages = int(ceil(hits / float(self.per_page))) + 1
        return self._num_pages
    num_pages = property(_get_num_pages)
        

class LazyPaginator(BasePaginator):
    def validate_number(self, number):
        try:
            number = int(number)
        except ValueError:
            raise PageNotAnInteger('That page number is not an integer')
        if number < 1:
            raise EmptyPage('That page number is less than 1')
        return number
        
    def page(self, number):
        number = self.validate_number(number)
        current_per_page = self.get_current_per_page(number)
        bottom = max((number-2)*self.per_page + self.first_page, 0)
        top = bottom + current_per_page
        # get more objects to see if there is a next page
        objects = list(self.object_list[bottom:top + self.orphans + 1])
        if len(objects) > (current_per_page + self.orphans):
            # if there is a next page increase the total number of pages
            self._num_pages = number + 1
            # but return only objects for this page
            objects = objects[:current_per_page]
        else:
            # this is the last page
            self._num_pages = number
        return CustomPage(objects, number, self)
        
    def _get_count(self):
        raise NotImplementedError
    count = property(_get_count)

    def _get_num_pages(self):
        return self._num_pages
    num_pages = property(_get_num_pages)

    def _get_page_range(self):
        raise NotImplementedError
    page_range = property(_get_page_range)
