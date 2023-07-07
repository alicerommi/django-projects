from scholarly import scholarly

class author_publication:
    def __init__(self,author_name):
        self.author_name = author_name
        self.search_query = scholarly.search_author(self.author_name)


    def crawler(self):
        first_author_result = next(self.search_query)
        author = scholarly.fill(first_author_result)

        publication_titles = [pub['bib']['title'] for pub in author['publications']]

        pub_titles = {
            'publication_titles': publication_titles
        }

        return  pub_titles



