from django.core.paginator import Paginator, Page, EmptyPage, PageNotAnInteger

class LazyPaginator(Paginator):
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
        bottom = (number - 1) * self.per_page
        top = bottom + self.per_page
        # get more objects to see if there is a next page
        objects = list(self.object_list[bottom:top + self.orphans + 1])
        if len(objects) > (self.per_page + self.orphans):
            # if there is a next page increase the total number of pages
            self._num_pages = number + 1
            # but return only objects for this page
            objects = objects[:self.per_page]
        else:
            # this is the last page
            self._num_pages = number
        return Page(objects, number, self)
        
    def _get_count(self):
        raise NotImplementedError
    count = property(_get_count)

    def _get_num_pages(self):
        return self._num_pages
    num_pages = property(_get_num_pages)

    def _get_page_range(self):
        raise NotImplementedError
    page_range = property(_get_page_range)
