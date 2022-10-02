from .models import LatexRenderCache
from .serializers import LatexRenderCacheSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
import urllib.parse
import matplotlib.pyplot as plt
from matplotlib import rcParams

# Enable latex support in matplotlib
rcParams['text.usetex'] = True


class RenderViewSet(viewsets.ModelViewSet):
    queryset = LatexRenderCache.objects.all()
    serializer_class = LatexRenderCacheSerializer

    @action(detail=False, methods=['get'])
    def render(self, request, pk=None):

        # Read the `ex` parameter from the request
        expression = request.query_params.get('ex', None)
        if not expression:
            return Response({'error': 'Missing ?ex parameter'}, status=400)

        # URL decode the expression
        expression = urllib.parse.unquote(expression)
        print(f"Got render request for expression: {expression}")

        # If the expression is already in the database, return it
        try:
            cache = LatexRenderCache.objects.get(expression=expression)
            return Response(cache.svg, content_type='image/svg+xml')
        except LatexRenderCache.DoesNotExist:
            pass

        # Use matplotlib to render the expression to SVG and save it to the database
        plt.text(0.0, 0.0, expression, fontsize=14)
        ax = plt.gca()
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)
        
        # Save the SVG to a string
        svg = plt.savefig('/tmp/render.svg', format='svg')
        
        # Save the SVG to the database
        cache = LatexRenderCache(expression=expression, svg=open('/tmp/render.svg', 'r').read())
        cache.save()
        
        # Return the SVG
        return Response(svg, content_type='image/svg+xml')