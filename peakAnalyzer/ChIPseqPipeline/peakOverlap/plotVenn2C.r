venn.overlap <- function(r, a, b, target = 0)
{
#
# calculate the overlap area for circles of radius a and b 
# with centers separated by r
# target is included for the root finding code
#
	pi = acos(-1)
	if(r >= a + b) {
		return( - target)
	}
	if(r < a - b) {
		return(pi * b * b - target)
	}
	if(r < b - a) {
		return(pi * a * a - target)
	}
	s = (a + b + r)/2
	triangle.area = sqrt(s * (s - a) * (s - b) * (s - r))
	h = (2 * triangle.area)/r
	aa = 2 * atan(sqrt(((s - r) * (s - a))/(s * (s - b))))
	ab = 2 * atan(sqrt(((s - r) * (s - b))/(s * (s - a))))
	sector.area = aa * (a * a) + ab * (b * b)
	overlap = sector.area - 2 * triangle.area
	return(overlap - target)
}

# takes in a list d
plot.venn.diagram <- function(d)
{
#
# Draw Venn diagrams with proportional overlaps
# d$table = 2 way table of overlaps
# d$labels = array of character string to use as labels
#
pi = acos(-1)
csz = 0.05
csz2 = 0.02
# Normalize the data
n = length(dim(d$table)) # 2 factors so n = 3?
c1 = vector(length = n)
c1[1] = sum(d$table[2,  ]) # total count of peak1

c1[2] = sum(d$table[, 2])  # total count of peak2
n1 = c1
#
c2 = matrix(nrow = n, ncol = n, 0) # create a matrix of 2 rows, 2 cols and value = 0
c2[1, 2] = sum(d$table[2, 2])  # overlap count
c2[2, 1] = c2[1, 2]
n2 = c2
#
c2 = c2/sum(c1)
c1 = c1/sum(c1)
n = length(c1)


# Radii are set so the area is proporitional to number of counts
pi = acos(-1)
r = sqrt(c1/pi)
r12=0
if(min(c1)==c2[1,2])
	r12=min(r) 
else if (c2[1,2]==0)
	r12=0
else
r12 = uniroot(venn.overlap, interval = c(max(r[1] - r[2], r[2] - r[1],
0) + 0.01, r[1] + r[2] - 0.01), a = r[1], b = r[
2], target = c2[1, 2])$root


s = r12/2 #correct?
x = vector()
y = vector()
x[1] = 0
y[1] = 0
x[2] = r12
y[2] = 0
xc = cos(seq(from = 0, to = 2 * pi, by = 0.01))
yc = sin(seq(from = 0, to = 2 * pi, by = 0.01))
cmx = sum(x * c1)
cmy = sum(y * c1)
x = x - cmx
y = y - cmy
rp=sqrt(x*x + y*y)

frame()
par(usr = c(-1, 1, -1, 1), pty = "s")

polygon(xc*r[1]+x[1], yc * r[1] + y[1], col="#0000ff70")
lines(xc*r[1]+x[1], yc * r[1] + y[1], col="#0000ff", lwd=2)
polygon(xc*r[2]+x[2], yc * r[2] + y[2], angle=180, col="#80000070")
lines(xc*r[2]+x[2], yc * r[2] + y[2], col="#800000", lwd=2)

legend("bottom","center",d$labels, col=c("#0000ff", "#800000"), pch=20, horiz=TRUE, pt.cex=2)

#print value
xl = (rp[1] + (0.7 * r[1])) * x[1]/rp[1]
yl = (rp[1] + (0.7 * r[1])) * y[1]/rp[1]
if(d$table[2,1]>0)
text(xl, yl, d$table[2,1])
xl = (rp[2] + (0.7 * r[2])) * x[2]/rp[2]
yl = (rp[2] + (0.7 * r[2])) * y[2]/rp[2]
if(d$table[1,2]>0)
text(xl, yl, d$table[1,2])

if(d$table[2,2]>0)
text((x[1] + x[2])/2 + csz, (y[1] + y[2])/2, d$table[2, 2]) #circle A and B intersect
list(r = r, x = x, y = y, dist = r12, count1 = c1, count2 =
c2, labels = d$labels)
}


Args<-commandArgs()[grep("^--",commandArgs(),invert=T)]

#main
inp = scan(Args[2], skip=1, list(first=0, second=0))
A = inp$first > 0
B = inp$second > 0
label = scan(Args[2], what="char", nlines = 1)


# Create a list which stores a table and labels.
d = list()
d$table <-matrix(0, 2, 2)

temp<-table(A,B)
if ("FALSE" %in% rownames(temp) && "FALSE" %in% colnames(temp)) 
d$table[1,1]=temp["FALSE","FALSE"]
if ("FALSE" %in% rownames(temp) && "TRUE" %in% colnames(temp))
d$table[1,2]=temp["FALSE","TRUE"]
if ("TRUE" %in% rownames(temp) && "FALSE" %in% colnames(temp))
d$table[2,1]=temp["TRUE","FALSE"]
if ("TRUE" %in% rownames(temp) && "TRUE" %in% colnames(temp))
d$table[2,2]=temp["TRUE","TRUE"]

d$table

d$labels = label
# Pass list d into the function plot.venn.diagram
png(paste(Args[2],".venn.png",sep = "")) ## set the device to print to png
plot.venn.diagram(d)
dev.off()
